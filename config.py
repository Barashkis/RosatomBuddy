from os import getenv
from dotenv import load_dotenv

load_dotenv()

token = getenv("TOKEN")
pg_user = getenv("PG_USER")
pg_pass = getenv("PG_PASS")
pg_host = getenv("PG_HOST")
pg_db_name = getenv("PG_DB_NAME")

divisions = ["Электроэнергетический",
             "Машиностроительный",
             "Горнорудный",
             "Ядерный оружейный комплекс",
             "Инжиниринговый",
             "Административно-хозяйственный отдел",
             "Наука и инновации",
             "Топливный",
             "Другой"]

companies = ["Корпоративная Академия Росатома",
             "ООО «НИИАР-ГЕНЕРАЦИЯ»",
             "Русатом — Международная сеть",
             "Государственная корпорация по атомной энергии «Росатом»",
             "Акционерное общество «АтомЭнергоСбыт»",
             "АО «Русатом Автоматизированные системы управления»",
             "АО «В/О «Изотоп»",
             "АО «Научно-исследовательский институт технической физики и автоматизации»",
             "Управление по работе с персоналом и организационному развитию Дирекции по ядерному оружейному комплексу",
             "ФГУП МОКБ «Марс»",
             "Центр карьеры госкорпорации «Росатом»",
             "Частное учреждение по цифровизации атомной отрасли «Цифрум»",
             "Филиал акционерного общества «Русатом Инфраструктурные решения» в городе Новоуральске",
             "ФГУП «Аварийно-технический центр Минатома России»",
             "АО «НПК Химпроминжиниринг»",
             "АО «Ветроэнергетическая отдельная генерирующая компания»",
             "АО «Опытно-демонстрационный центр вывода из эксплуатации уран-графитовых реакторов»",
             "АО «Ордена Трудового Красного Знамени научно-исследовательский физико-химический институт имени Л. Я. Карпова»",
             "АО «Русатом Оверсиз»",
             "ФГУП «Атомфлот»",
             "ФГУП «Горно-химический комбинат»",
             "ФГУП «Предприятие по обращению с радиоактивными отходами «РосРАО»",
             "ФГУП «Объединенный эколого-технологический и научно-исследовательский центр по обезвреживанию РАО и охране окружающей среды»",
             "ФГУП «Ситуационно-Кризисный Центр Федерального агентства по атомной энергии»"]
