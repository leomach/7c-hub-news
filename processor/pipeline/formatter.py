from datetime import datetime
from typing import List
from processor.models.news_item import NewsItem

DIAS_SEMANA = {
    0: "Segunda-feira", 1: "Terça-feira", 2: "Quarta-feira",
    3: "Quinta-feira", 4: "Sexta-feira", 5: "Sábado", 6: "Domingo"
}

MESES = {
    1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril",
    5: "maio", 6: "junho", 7: "julho", 8: "agosto",
    9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro"
}

def format_bulletin(items: List[NewsItem], date: datetime) -> str:
    dia_semana = DIAS_SEMANA[date.weekday()]
    data_formatada = f"{date.day} de {MESES[date.month]} de {date.year}"
    
    header = f"🗞 <b>7C Hub News</b> — {dia_semana}, {data_formatada}\n"
    header += "━━━━━━━━━━━━━━━━━━━━\n\n"
    
    global_items = [i for i in items if i.source_category == "global"]
    national_items = [i for i in items if i.source_category == "national"]
    regional_items = [i for i in items if i.source_category == "regional"]
    
    body = ""
    counter = 1
    
    if global_items:
        body += "🌍 <b>MUNDO</b>\n\n"
        for item in global_items:
            body += f"{get_emoji(counter)} <b>{item.title_pt or item.title}</b>\n"
            body += f"<i>{item.summary_pt or item.summary_original or ''}</i>\n"
            body += f"🔗 {item.url}\n\n"
            counter += 1
            
    if national_items:
        body += "━━━━━━━━━━━━━━━━━━━━\n"
        body += "🇧🇷 <b>BRASIL</b>\n\n"
        for item in national_items:
            body += f"{get_emoji(counter)} <b>{item.title_pt or item.title}</b>\n"
            body += f"<i>{item.summary_pt or item.summary_original or ''}</i>\n"
            body += f"🔗 {item.url}\n\n"
            counter += 1
            
    if regional_items:
        body += "━━━━━━━━━━━━━━━━━━━━\n"
        body += "📍 <b>PERNAMBUCO & REGIÃO</b>\n\n"
        for item in regional_items:
            body += f"{get_emoji(counter)} <b>{item.title_pt or item.title}</b>\n"
            body += f"<i>{item.summary_pt or item.summary_original or ''}</i>\n"
            body += f"🔗 {item.url}\n\n"
            counter += 1
            
    footer = "━━━━━━━━━━━━━━━━━━━━\n"
    footer += "<i>Boletim gerado automaticamente pelo 7C Hub News Bot</i> 🤖"
    
    return header + body + footer

def get_emoji(n: int) -> str:
    emojis = {1: "1️⃣", 2: "2️⃣", 3: "3️⃣", 4: "4️⃣", 5: "5️⃣", 6: "6️⃣", 7: "7️⃣", 8: "8️⃣", 9: "9️⃣"}
    return emojis.get(n, str(n))
