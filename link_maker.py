def link_maker(): 
        with open('ffsid.txt',mode='r') as file: 
            ids= file.readlines()
            print(ids)  

        for id in ids: 
            link = f"https://www.flipkart.com/product/p/item?pid={id.strip()}"
            print(link)

link_maker()