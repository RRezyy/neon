import requests
from bs4 import BeautifulSoup
from threading import Thread

def check_Bin(Bin):
    url = f"https://binlist.io/lookup/{Bin}"
    datas = requests.get(url).json()

    if datas['success'] == True:
        Message = (f"Bin      :  {Bin}\n"
                             f"Scheme   :  {datas['scheme']}\n"
                             f"Country  :  {datas['country']['name']}\n"
                             f"Type     :  {datas['type']}\n"
                             f"Category :  {datas['category']}\n"
                             f"Bank     :  {datas['bank']['name']}")
        return Message
    else:
        Message = "bin is not valid"
        return Message

def get_data(Country):
    if Country == "de" or Country == "us" or Country == "gb" or Country == "it":
        url = f"https://fakeit.receivefreesms.co.uk/c/{Country}"
        response = requests.get(url)

        soup = BeautifulSoup(response.content, "html.parser")
        
        card_body_elements = soup.find_all(class_="card-body")
        if len(card_body_elements) >= 2:
            second_card_body = card_body_elements[1]
            details = []
            elements = second_card_body.find_all(["td", "th"])
            for i in range(0, len(elements), 2):
                label = elements[i].get_text(strip=True)
                value = elements[i + 1].get_text(strip=True)
                
                if label and value:
                    details.append(f"{label}: {value}\n")

            if details:
                return "\n".join(details)
            else:
                return "Error: No financial details found. The section must be truly elusive!"
        else:
            return "Error: The second card-body element is missing. Those details are good at hiding."