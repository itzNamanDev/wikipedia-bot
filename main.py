import pywikibot
import re

# Define the bot class
class CitationFixerBot:
    def __init__(self, site):
        self.site = site
        self.repo = site.data_repository()

    def run(self):
        # Define the category or articles to process
        category = pywikibot.Category(self.site, "Category:Articles_with_bare_URLs_for_citations")
        for page in category.articles():
            print(f"Processing: {page.title()}")
            self.process_page(page)

    def process_page(self, page):
        try:
            text = page.text
            updated_text = self.fix_bare_urls(text)
            if updated_text != text:
                page.text = updated_text
                page.save(summary="Fixing bare URLs by adding citation templates")
                print(f"Updated: {page.title()}")
            else:
                print(f"No changes needed for: {page.title()}")
        except Exception as e:
            print(f"Error processing {page.title()}: {e}")

    def fix_bare_urls(self, text):
        # Regular expression to find bare URLs
        bare_url_pattern = r'(http[s]?://[^\s]+)'
        matches = re.findall(bare_url_pattern, text)
        
        for url in matches:
            if "cite web" not in text:  # Avoid overwriting existing citations
                citation_template = f"{{{{cite web |url={url} |title= |access-date= |website= }}}}"
                text = text.replace(url, citation_template)
        
        return text

# Main execution
def main():
    site = pywikibot.Site("en", "wikipedia")
    bot = CitationFixerBot(site)
    bot.run()

if __name__ == "__main__":
    main()
