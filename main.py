from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Словарь для хранения задач каждого пользователя
user_tasks = {}

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
        user_id = update.message.from_user.id
        if user_id not in user_tasks:
            user_tasks[user_id] = []
        await update.message.reply_text(instruction, reply_markup=markup)

async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        user_id = update.message.from_user.id
        task = ' '.join(context.args)
        if task:
            user_tasks[user_id].append({"task": task, "done": False})
            await update.message.reply_text(f'Task "{task}" added.', reply_markup=markup)
        else:
            await update.message.reply_text('Please provide a task description after the /add command.', reply_markup=markup)

async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        user_id = update.message.from_user.id
        if user_id in user_tasks and user_tasks[user_id]:
            message = 'Task list:\n'
            for i, task in enumerate(user_tasks[user_id]):
                status = "completed" if task["done"] else "not completed"
                message += f'{i+1}. {task["task"]} - {status}\n'
            await update.message.reply_text(message, reply_markup=markup)
        else:
            await update.message.reply_text('Task list is empty.', reply_markup=markup)

async def done_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        user_id = update.message.from_user.id
        try:
            task_number = int(context.args[0]) - 1
            if 0 <= task_number < len(user_tasks[user_id]):
                user_tasks[user_id][task_number]["done"] = True
                await update.message.reply_text(f'Task "{user_tasks[user_id][task_number]["task"]}" marked as completed.', reply_markup=markup)
            else:
                await update.message.reply_text('Invalid task number.', reply_markup=markup)
        except (IndexError, ValueError):
            await update.message.reply_text('Please provide the task number after the /done command.', reply_markup=markup)

async def delete_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        user_id = update.message.from_user.id
        try:
            task_number = int(context.args[0]) - 1
            if 0 <= task_number < len(user_tasks[user_id]):
                deleted_task = user_tasks[user_id].pop(task_number)
                await update.message.reply_text(f'Task "{deleted_task["task"]}" deleted.', reply_markup=markup)
            else:
                await update.message.reply_text('Invalid task number.', reply_markup=markup)
        except (IndexError, ValueError):
            await update.message.reply_text('Please provide the task number after the /delete command.', reply_markup=markup)

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
