import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from fpdf import FPDF

# States for the conversation
DATE, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, CONFIRM = range(10)

# Initialize responses
responses = {}

# Microsoft Form URL
form_url = "https://forms.office.com/r/1amQJafpFG"
def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Welcome! Please enter the date (YYYY-MM-DD):")
    return DATE

def date(update: Update, context: CallbackContext) -> int:
    responses['date'] = update.message.text
    update.message.reply_text("Question 2: [MCQ] Choose an option.", reply_markup=ReplyKeyboardMarkup([['Option 1', 'Option 2']], one_time_keyboard=True))
    return Q2

def q2(update: Update, context: CallbackContext) -> int:
    responses['q2'] = update.message.text
    update.message.reply_text("Question 3: [MCQ] Choose an option.", reply_markup=ReplyKeyboardMarkup([['Option 1', 'Option 2']], one_time_keyboard=True))
    return Q3

def q3(update: Update, context: CallbackContext) -> int:
    responses['q3'] = update.message.text
    update.message.reply_text("Question 4: [MCQ] Choose an option.", reply_markup=ReplyKeyboardMarkup([['Option 1', 'Option 2']], one_time_keyboard=True))
    return Q4

def q4(update: Update, context: CallbackContext) -> int:
    responses['q4'] = update.message.text
    update.message.reply_text("Question 5: Please provide a long text answer.")
    return Q5

def q5(update: Update, context: CallbackContext) -> int:
    responses['q5'] = update.message.text
    update.message.reply_text("Question 6: Please provide a long text answer.")
    return Q6

def q6(update: Update, context: CallbackContext) -> int:
    responses['q6'] = update.message.text
    update.message.reply_text("Question 7: Please provide a long text answer.")
    return Q7

def q7(update: Update, context: CallbackContext) -> int:
    responses['q7'] = update.message.text
    update.message.reply_text("Question 8: Please provide a long text answer.")
    return Q8

def q8(update: Update, context: CallbackContext) -> int:
    responses['q8'] = update.message.text
    update.message.reply_text("Question 9: Please provide a long text answer.")
    return Q9

def q9(update: Update, context: CallbackContext) -> int:
    responses['q9'] = update.message.text
    update.message.reply_text("Do you want to review your answers? (yes/no)")
    return CONFIRM

def confirm(update: Update, context: CallbackContext) -> int:
    if update.message.text.lower() == 'yes':
        review_responses(update, context)
        update.message.reply_text("You can go back and edit any answer by typing the question number (e.g., Q2).")
    else:
        submit_responses()
        update.message.reply_text("Your responses have been submitted.")
        generate_pdf()
        context.bot.send_document(chat_id=update.message.chat_id, document=open("responses.pdf", "rb"))
    return ConversationHandler.END

def review_responses(update, context):
    for q, a in responses.items():
        update.message.reply_text(f"{q}: {a}")

def submit_responses():
    options = Options()
    options.headless = True
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(form_url)

    # Fill in the form fields
    date_field = driver.find_element(By.XPATH, '//input[@type="date"]')
    date_field.send_keys(responses['date'])
    
    q2_option = driver.find_element(By.XPATH, f'//input[@value="{responses["q2"]}"]')
    q2_option.click()
    
    q3_option = driver.find_element(By.XPATH, f'//input[@value="{responses["q3"]}"]')
    q3_option.click()
    
    q4_option = driver.find_element(By.XPATH, f'//input[@value="{responses["q4"]}"]')
    q4_option.click()
    
    q5_field = driver.find_element(By.XPATH, '(//textarea)[1]')
    q5_field.send_keys(responses['q5'])
    
    q6_field = driver.find_element(By.XPATH, '(//textarea)[2]')
    q6_field.send_keys(responses['q6'])
    
    q7_field = driver.find_element(By.XPATH, '(//textarea)[3]')
    q7_field.send_keys(responses['q7'])
    
    q8_field = driver.find_element(By.XPATH, '(//textarea)[4]')
    q8_field.send_keys(responses['q8'])
    
    q9_field = driver.find_element(By.XPATH, '(//textarea)[5]')
    q9_field.send_keys(responses['q9'])
    
    submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    submit_button.click()
    
    driver.quit()

def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for q, a in responses.items():
        pdf.cell(200, 10, txt=f"{q}: {a}", ln=True)
    pdf.output("responses.pdf")

def main():
    token = os.getenv(6531059902:AAFWL-dyRtV0uHpG1Ch9IkE5IFZzSqWeh8E)
    if not token:
        raise ValueError("No TELEGRAM_BOT_TOKEN provided")
    
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            DATE: [MessageHandler(Filters.text & ~Filters.command, date)],
            Q2: [MessageHandler(Filters.text & ~Filters.command, q2)],
            Q3: [MessageHandler(Filters.text & ~Filters.command, q3)],
            Q4: [MessageHandler(Filters.text & ~Filters.command, q4)],
            Q5: [MessageHandler(Filters.text & ~Filters.command, q5)],
            Q6: [MessageHandler(Filters.text & ~Filters.command, q6)],
            Q7: [MessageHandler(Filters.text & ~Filters.command, q7)],
            Q8: [MessageHandler(Filters.text & ~Filters.command, q8)],
            Q9: [MessageHandler(Filters.text & ~Filters.command, q9)],
            CONFIRM: [MessageHandler(Filters.text & ~Filters.command, confirm)],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()


