class AmbilData:
    def __init__(self,link_url=None, user=None):
        self.link_url = link_url
        self.user = {
            'User-Agent': str(user+"/1.0 ()")
        }
        self.data = None
    
    def konek_data(self):
        import requests
        url = self.link_url
        profil = self.user
        if url is not None and profil is not None:
            response = url
            try:
                data = requests.get(response, headers=profil)
                if data.status_code == 200:
                    print("Berhasil terhubung ke server data")
                else:
                    print(f"Gagal dengan kode: {data.status_code}")
                self.data = data
            except Exception as e:
                print(e)

    def ambil_data(self):
        import requests
        data = self.data
        if (data is not None):
            try:
                data = data.content.decode('utf-8')
                print(data[:1000])
                self.data = data
            except Exception as e:
                print(e)

    def urai_data(self):
        from bs4 import BeautifulSoup
        data = self.data
        if data is not None:
            soup = BeautifulSoup(data, "lxml")
            konten = soup.find('div', class_='mw-parser-output') 
            def memebersihkan_konten(node_konten):
                """Menghapus elemen non-artikel umum"""
                selectors = [
                '.mw-jump-link',
                '.navbox',
                '.reflist',
                'sup.reference',
                '.mw-editsection',
                '.hatnote',
                '.metadata',
                '.infobox',
                '#toc',
                '.toc',
                '.sidebar',
            ]
                for selector in selectors:
                    for el in node_konten.select(selector):
                        el.decompose()   

            if konten:
                memebersihkan_konten(konten)
                data = konten.get_text(separator=' ', strip=True)
                print(data[:1000])    
                self.data = data
            else:
                print("Tidak dapat menemukan konten utama")
                data = konten.get_text(separator=' ', strip=True)
                print(data[:1000])

    def ambil_insight(self):
        import nlp_rake
        data = self.data
        ekstraktor = nlp_rake.Rake(max_words=2, min_freq=3, min_chars=5)
        hasil = ekstraktor.apply(data)
        self.data = hasil
        return hasil
    
class Visualisasi:
    def __init__(self, data=None, batas=None):
        self.data = data
        self.batas = batas

    def bar_chart(self):
        import matplotlib.pyplot as plt
        batas = self.batas
        data_teratas = self.data[:batas]
        k, v = zip(*data_teratas)
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(k)),v)
        plt.xticks(range(len(k)),k,rotation='vertical')
        if batas is not None:
            plt.title(f"Top {batas} Kata Kunci Teratas")
        plt.tight_layout()
        plt.show()
    
    def wordcloud_maker(self):
        from wordcloud import WordCloud
        import matplotlib.pyplot as plt
        batas = self.batas
        data_teratas = self.data[:batas]
        wc = WordCloud(background_color='white', width=800, height=600)
        plt.figure(figsize=(15,7))
        plt.imshow(wc.generate_from_frequencies({k:v for k,v in data_teratas}))
        if batas is not None:
            plt.title(f"Top {batas} Kata Kunci Teratas")
        plt.axis("off")
        plt.show()
        return wc


        
    







if __name__ == '__main__':
    url = AmbilData("https://en.wikipedia.org/wiki/Machine_learning", "BelajarDataScience")
    url.konek_data() 
    print("="*50, "\n")  
    url.ambil_data()
    print("="*50, "\n")  
    url.urai_data()
    print("="*50, "\n")  
    hasil_insight = url.ambil_insight()
    print(hasil_insight)

    img = Visualisasi(hasil_insight, 10)
    # img.bar_chart()
    img.wordcloud_maker()


        


