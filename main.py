from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Список для хранения задач
tasks = []

# Определение кнопок
reply_keyboard = [['/list']]

# Создание разметки клавиатуры
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

instruction = """
Welcome! I am a task management bot. Use the buttons below to interact with me.

Commands:
1. /start - Start the bot and show this instruction.
2. /add <task description> - Add a new task.
   Example: /add Buy groceries
3. /list - Show all tasks with their status.
4. /done <task number> - Mark a task as completed.
   Example: /done 1
5. /delete <task number> - Delete a task.
   Example: /delete 1
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(instruction, reply_markup=markup)

async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        task = ' '.join(context.args)
        if task:
            tasks.append({"task": task, "done": False})
            await update.message.reply_text(f'Задача "{task}" добавлена.', reply_markup=markup)
        else:
            await update.message.reply_text('Пожалуйста, укажите описание задачи после команды /add.', reply_markup=markup)

async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        if tasks:
            message = 'Список задач:\n'
            for i, task in enumerate(tasks):
                status = "выполнена \U00002705" if task["done"] else "не выполнена \U0000274C"
                message += f'{i+1}. {task["task"]} - {status}\n'
            await update.message.reply_text(message, reply_markup=markup)
        else:
            await update.message.reply_text('Список задач пуст.', reply_markup=markup)

async def done_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        try:
            task_number = int(context.args[0]) - 1
            if 0 <= task_number < len(tasks):
                tasks[task_number]["done"] = True
                await update.message.reply_text(f'Задача "{tasks[task_number]["task"]}" отмечена как выполненная.', reply_markup=markup)
            else:
                await update.message.reply_text('Неверный номер задачи.', reply_markup=markup)
        except (IndexError, ValueError):
            await update.message.reply_text('Пожалуйста, укажите номер задачи после команды /done.', reply_markup=markup)

async def delete_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        try:
            task_number = int(context.args[0]) - 1
            if 0 <= task_number < len(tasks):
                removed_task = tasks.pop(task_number)
                await update.message.reply_text(f'Задача "{removed_task["task"]}" удалена.', reply_markup=markup)
            else:
                await update.message.reply_text('Неверный номер задачи.', reply_markup=markup)
        except (IndexError, ValueError):
            await update.message.reply_text('Пожалуйста, укажите номер задачи после команды /delete.', reply_markup=markup)

def main() -> None:
    # Введите здесь токен вашего бота
    application = ApplicationBuilder().token("7221478109:AAG4PVdAQHbMXlZWoGpg7pViwMYitVHdTQI").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add_task))
    application.add_handler(CommandHandler("list", list_tasks))
    application.add_handler(CommandHandler("done", done_task))
    application.add_handler(CommandHandler("delete", delete_task))

    application.run_polling()

if __name__ == '__main__':
    main()


