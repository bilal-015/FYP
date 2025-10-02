from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
import pandas as pd
import time
import re
import numpy as np


class MCQScraper:
    def __init__(self, driver_path: str):
        """Initialize Chrome WebDriver"""
        s = Service(driver_path)
        self.driver = webdriver.Chrome(service=s)

    def get_links(self, main_url: str) -> list:
        """Scrape all href links from the given Sanfoundry main page"""
        print(f"🌍 Opening main page: {main_url}")
        self.driver.get(main_url)
        time.sleep(2)  # wait for page load
        div = self.driver.find_element(By.CSS_SELECTOR, ".textwidget.custom-html-widget")
        a_tags = div.find_elements(By.TAG_NAME, "a")
        hrefs = [a.get_attribute("href") for a in a_tags if a.get_attribute("href")]
        print(f"✅ Found {len(hrefs)} links")
        return hrefs

    def scrape_mcqs(self, hrefs: list) -> pd.DataFrame:
        """Scrape all MCQs from given list of URLs and return as DataFrame"""
        all_dataframes = []

        for idx, url in enumerate(hrefs):
            print(f"\n🔗 Processing URL {idx + 1}/{len(hrefs)}: {url}")

            try:
                self.driver.get(url)
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.entry-content"))
                )
                print("✅ Page loaded successfully")
            except (WebDriverException, TimeoutException) as e:
                print(f"❌ Failed to load URL: {url}\nError: {e}")
                continue

            # Expand all answers
            try:
                buttons = self.driver.find_elements(By.CLASS_NAME, "collapseomatic")
                for btn in buttons:
                    try:
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                        time.sleep(0.3)
                        btn.click()
                        time.sleep(0.3)
                    except:
                        continue
            except:
                pass

            # Initialize containers
            q_number, q_text, code_part, opt_a, opt_b, opt_c, opt_d, correct_ans, explanation = [], [], [], [], [], [], [], [], []

            content_div = self.driver.find_element(By.CSS_SELECTOR, "div.entry-content")
            children = content_div.find_elements(By.XPATH, "./*")

            i = 0
            while i < len(children):
                el = children[i]
                tag = el.tag_name
                html = el.get_attribute("innerHTML")

                # --- Case 1: Questions without code blocks ---
                if tag == "p" and "View Answer" in html and "<br>" in html and re.search(r"^\d+\.\s*[^<]{3,}", html):
                    try:
                        match = re.split(r"\ba\)", html, maxsplit=1)
                        if len(match) < 2:
                            raise ValueError("Missing option a)")

                        question_line = match[0].replace("<br>", "").strip()
                        options_part = match[1].strip()
                        qnum = question_line[:2].strip()
                        qbody = question_line[3:].strip()

                        q_number.append(qnum)
                        q_text.append(qbody)

                        lines = options_part.split("<br>")
                        opt_a.append(lines[0].replace("a)", "").strip() if len(lines) > 0 else np.nan)
                        opt_b.append(lines[1].replace("b)", "").strip() if len(lines) > 1 else np.nan)
                        opt_c.append(lines[2].replace("c)", "").strip() if len(lines) > 2 else np.nan)
                        opt_d.append(lines[3].replace("d)", "").strip() if len(lines) > 3 else np.nan)

                        # Answer & explanation
                        collapse = el.find_element(By.CLASS_NAME, "collapseomatic")
                        div_id = collapse.get_attribute("id")
                        target_div = self.driver.find_element(By.ID, f"target-{div_id}")
                        ans_html = target_div.get_attribute("innerHTML").split("<br>")

                        ans = ans_html[0].replace("Answer:", "").strip() if len(ans_html) > 0 else np.nan
                        expl = ans_html[1].replace("Explanation:", "").strip() if len(ans_html) > 1 else np.nan

                        correct_ans.append(ans)
                        explanation.append(expl)
                        code_part.append(np.nan)

                    except Exception as e:
                        print(f"❌ Skipping question due to error: {e}")
                        continue
                    i += 1
                    continue

                # --- Case 2: Questions with code blocks ---
                if tag == "div" and "hk1_style" in el.get_attribute("class"):
                    try:
                        prev_p = el.find_element(By.XPATH, "preceding-sibling::p[1]")
                        prev_html = prev_p.get_attribute("innerHTML")
                        prev_html_clean = re.sub(r"<.*?>", "", prev_html).strip()

                        q_match = re.match(r"^(\d+)\.\s*(.*)", prev_html_clean)
                        if not q_match:
                            raise ValueError("❌ Question text or number not found.")
                        qnum = q_match.group(1)
                        qtext = q_match.group(2)

                        code_lines = el.find_elements(By.CSS_SELECTOR, "pre.de1")
                        code = "\n".join([line.text.strip() for line in code_lines if line.text.strip()]) or np.nan

                        next_p = el.find_element(By.XPATH, "following-sibling::p[1]")
                        options_html = next_p.get_attribute("innerHTML")
                        opt_lines = options_html.split("<br>")
                        a = opt_lines[0].replace("a)", "").strip() if len(opt_lines) > 0 else np.nan
                        b = opt_lines[1].replace("b)", "").strip() if len(opt_lines) > 1 else np.nan
                        c = opt_lines[2].replace("c)", "").strip() if len(opt_lines) > 2 else np.nan
                        d = opt_lines[3].replace("d)", "").strip() if len(opt_lines) > 3 else np.nan

                        next_div = next_p.find_element(By.XPATH, "following-sibling::div[1]")
                        answer_html = next_div.get_attribute("innerHTML").split("<br>")
                        answer = answer_html[0].replace("Answer:", "").strip() if len(answer_html) > 0 else np.nan
                        exp = answer_html[1].replace("Explanation:", "").strip() if len(answer_html) > 1 else np.nan

                        q_number.append(qnum)
                        q_text.append(qtext)
                        code_part.append(code)
                        opt_a.append(a)
                        opt_b.append(b)
                        opt_c.append(c)
                        opt_d.append(d)
                        correct_ans.append(answer)
                        explanation.append(exp)

                    except Exception as ex:
                        print(f"⚠️ Skipped due to error: {ex}")

                i += 1

            # Build dataframe
            df = pd.DataFrame({
                "Q_No": q_number,
                "Question": q_text,
                "Code_Part": code_part,
                "Option_A": opt_a,
                "Option_B": opt_b,
                "Option_C": opt_c,
                "Option_D": opt_d,
                "Answer": correct_ans,
                "Explanation": explanation
            })

            all_dataframes.append(df)
            print(f"✅ Data scraped from URL {idx + 1}: {url}")

        # Combine & return DataFrame
        final_df = pd.concat(all_dataframes, ignore_index=True)
        return final_df

    def close(self):
        """Close the browser driver"""
        self.driver.quit()




if __name__ == "__main__":
    scraper = MCQScraper(driver_path="D:\\FYP\\datasets\\chromedriver-win64\\chromedriver.exe")

    # Step 1: Get all links
    hrefs = scraper.get_links("https://www.sanfoundry.com/object-oriented-programming-questions-answers-oops-features/")

    # Step 2: Scrape MCQs (now returns a DataFrame instead of writing CSV)
    df = scraper.scrape_mcqs(hrefs)

    # Step 3: Work with DataFrame in memory
    print(df.head())

    # Step 4: Optionally save if needed
    df.to_csv("newallOOPMCQs.csv", index=False)

    scraper.close()
