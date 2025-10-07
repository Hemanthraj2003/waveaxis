import time
from selenium import webdriver
from selenium.webdriver.common.by import By

articlesDict = {}

# Extracts the title and first 3 paragraphs of the article and stores it in a dictionary
def getArticleContent(driver):
    content = []
    
    # workaournd to fix the signup pop up
    time.sleep(1)
    driver.refresh() # refreshing the page removes the popup to signup 
    
    try:
        # content of the articles are within divs with data-component='text-block' attributes
        text_blocks = driver.find_elements(By.XPATH, "//div[@data-component='text-block']")
        
        # limiting to first 3 text blocks
        for block in text_blocks[:3]:
            paras = block.find_elements(By.TAG_NAME, "p")
            for para in paras:
                if para.text.strip():
                    content.append(para.text)
        
        # joining the list of paras and storing in the dictionary with title as key 
        articlesDict[driver.title] = "\n".join(content)
    
    except Exception as e:
        print(f"Error extracting content: {e}")

    
# Writes the articlesDict to a text file in a readable format
def writeToFile():
    with open("./articles.txt", "w") as f:
        for title, content in articlesDict.items():
            f.write("\n" + "="*(len(title) + 3) + "\n")
            f.write(f"Title:\n{title}")
            f.write("\n" + "="*(len(title) + 3) + "\n")
            f.write(f"Content:\n{content}\n\n\n")
            f.write("-"*50 + "\n\n")    


def get3Articles(driver):
    # n is the number of clickable articles found and processed
    # i is the number of current article being processed
    n,i = 0,0 
    
    while n<3: 
        # loop until 3 articles are processed
        try:
            # every article post shared a common pattern in their href "news/articels/:id"
            articles = driver.find_elements(By.XPATH, "//a[contains(@href, 'news/articles')]") 
            
            # to check if we are past the number of articles available
            if i >= len(articles):
                print("Ran Out of articles to open")
                break
            
            # Scroll to the article to make it clickable
            # (some articles were throwing ElementNotInteractableException because they were not in the viewport)
            # Offseting by 100 pixel because of the sticky navbar that covers the content which makes the article unclickable
            
            driver.execute_script("window.scrollTo(0, arguments[0].offsetTop - 100);", articles[i])
            
            # checking if the article is displayed because some articles had duplicate anchor tags which were hidden
            # and casuing ElementNotInteractableException, so this contidtion filters out those hidden articels
            if articles[i].is_displayed() and articles[i].is_enabled():
                try:
                    articles[i].click()
                    getArticleContent(driver) 
                    driver.back()
                    n += 1 # incrementing the count of articles processed
                
                except Exception as e:
                    print(e)
        
        except Exception as e:
            print(f"Error while processing article {i+1}: {e}")
        finally:
            i += 1 


def main():
    newSite = "https://www.bbc.com/"
    
    driver = webdriver.Chrome() # opens a chrome browser
    driver.get(newSite) # navigates to the news site
    
    try:
        get3Articles(driver)
        writeToFile()
        
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        driver.quit() # ensures the browser is closed after execution


if __name__ == "__main__":
    main()
    