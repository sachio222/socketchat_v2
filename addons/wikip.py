import wikipedia

class WikiArticle():
    def __init__(self):
        self.res = {}
    
    def run_from_cli(self, msg: list) -> str:
        """Joins msg parts, returns str"""
        try:
            query = ' '.join(msg[1:])
            self.input_query(query)
        except:
            self.input_query()

    def input_query(self, query:str = None) -> str:
        if not query:
            self.print_title()
            query = input('-+- New search: ')
        
        self.lookup(query)
        return query

    def lookup(self, query) -> None:
        try:
            r = wikipedia.search(query)
            s = wikipedia.summary(query, sentences=2)
            p = wikipedia.page(query)
            self.print(r, s, p)
        except Exception as e:
            print(e)
            pass

    def print(self, r, s, p) -> None:
        self.res = {}
        self.res = self.print_header(r)
        self.print_summary(s, p)
        self.show_options(p, self.res)

    def print_title(self):
        print('*****************')
        print('-=- Wikipedia -=-')
        print('*****************\n')

    def print_header(self, r) -> dict:
        self.print_title()
        print('-=- Matching Results -=-')

        for i, _r in enumerate(r, 1):
            print(f'{i}: {_r}')
            self.res[i] = _r

        return self.res

    def print_summary(self, s, p) -> None:
        print('\n-=- Top Hit -=-')
        print('Title:\t', p.title)
        print('Page:\t', p.url)
        print('\n-=- Summary -=-\n', s)
    
    def print_full(self, p) -> None:
        """Prints full article"""
        print('\n-=- Content -=- \n', p.content)
        self.show_options(p, self.res)
    
    def print_links(self, p):
        self.res = {}
        print("-=- Related Topics -=- ")
        for i, link in enumerate(p.links):
            print(f'{i}: {link}')
            self.res[i] = link
        self.show_options(p, self.res)
    
    def show_options(self, p, results: dict) -> None:
        print('\n-=- Options -=-')
        print('-=- (f) Show full article')
        print(f'-=- (#) See another article (1-{len(results)})')
        print('-=- (n) New search')
        print('-=- (t) Related topics')
        print('-=- (q) quit')
        choice = input('-=- Choice: ')
        if choice in ('f', 'F'):
            self.print_full(p)
        elif choice in ('n', 'N'):
            self.input_query()
        elif choice in ('t', 'T'):
            self.print_links(p)
        elif choice in ('q', 'Q'):
            print('*** Back to Chat ***')
            pass
        else:
            try:
                if int(choice):
                    while choice not in ('q', 'Q'):
                        if int(choice) in(results):
                            print('Getting summary for:', results[int(choice)])
                            self.lookup(results[int(choice)])
                            break
                        else:
                            print('Input a valid result from 1-10 or (q) to quit.')
                            choice = input('Result: ')
            except:
                print('Sorry, Invalid option, Quitting.')

                

    def show_links(self, p):
        print(p.links)

if __name__ == "__main__":
    wiki = WikiArticle()
    wiki.run_from_cli(['/msg', 'Roger',  'Moore'])
