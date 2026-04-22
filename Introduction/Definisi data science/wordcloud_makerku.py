import requests
from bs4 import BeautifulSoup
import nlp_rake
import matplotlib.pyplot as plt
from wordcloud import WordCloud


class AmbilData:
    def __init__(self,link_url=None, user=None):
        self.link_url = link_url
        self.user = {
            'User-Agent': str(user+"/1.0 ()")
        }
        self.response_obj = None   # Untuk objek Response dari requests
        self.html_content = None   # Untuk teks HTML mentah (String)
        self.clean_text = None     # Untuk teks bersih hasil BeautifulSoup (String)
        self.insight_result = None # Untuk List/Tuples hasil dari nlp_rake
    
    def konek_data(self):
        url = self.link_url
        profil = self.user
        if url is not None and profil is not None:
            # response = url
            try:
                response = requests.get(url, headers=profil)
                # data = requests.get(response, headers=profil)
                if response.status_code == 200:
                    print("Berhasil terhubung ke server data")
                else:
                    print(f"Gagal dengan kode: {response.status_code}")
                self.response_obj = response
            except requests.exceptions.HTTPError as http_err:
                print(f"Gagal: Server mengembalikan HTTP error: {http_err}")
            except requests.exceptions.ConnectionError as conn_err:
                print(f"Gagal: Tidak bisa menyambung ke server (Cek koneksi/URL): {conn_err}")
            except requests.exceptions.Timeout as timeout_err:
                print(f"Gagal: Waktu koneksi habis (Timeout): {timeout_err}")
            except requests.exceptions.RequestException as req_err:
                print(f"Gagal: Terjadi kesalahan pada requests: {req_err}")

    def ambil_data(self):
        if self.response_obj is not None:
            try:
                html_text = self.response_obj.content.decode('utf-8')
                print(f"Berhasil decode data HTML. Panjang karakter: {len(html_text)}")
                self.html_content = html_text
            except UnicodeDecodeError as decode_err:
                print(f"Gagal: Teks tidak bisa dibaca dengan format UTF-8: {decode_err}")
            except AttributeError as attr_err:
                print(f"Gagal: Objek respons tidak valid: {attr_err}")

    def urai_data(self):
        if self.html_content is not None:
            soup = BeautifulSoup(self.html_content, "lxml")
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
                teks_bersih = konten.get_text(separator=' ', strip=True)
                print(teks_bersih[:500] + "...\n[Teks Dipotong]")    
                self.clean_text = teks_bersih
            else:
                print("Peringatan: Elemen 'mw-parser-output' tidak ditemukan di halaman ini.")
                print("Mengamankan aliran data dengan memberikan string kosong.")
                self.clean_text = ""


    def ambil_insight(self):
        if self.clean_text:
            ekstraktor = nlp_rake.Rake(max_words=2, min_freq=3, min_chars=5)
            hasil = ekstraktor.apply(self.clean_text)
            self.insight_result = hasil
            return hasil
        else:
            print("Teks bersih belum tersedia. Harap jalankan urai_data() terlebih dahulu.")
            return None
    
class Visualisasi:
    def __init__(self, data=None, batas=None):
        self.data = data
        self.batas = batas

    def bar_chart(self):
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


        


