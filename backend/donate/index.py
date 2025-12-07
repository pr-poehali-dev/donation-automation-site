import json
import os
import psycopg2
import requests
from typing import Dict, Any

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    '''
    Обрабатывает заявки на донат: сохраняет в БД и отправляет уведомление администратору в Telegram
    Args: event - dict с httpMethod, body, queryStringParameters
          context - объект с атрибутами request_id, function_name
    Returns: HTTP response dict
    '''
    method: str = event.get('httpMethod', 'GET')
    
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Max-Age': '86400'
            },
            'body': '',
            'isBase64Encoded': False
        }
    
    if method == 'POST':
        body_data = json.loads(event.get('body', '{}'))
        nickname = body_data.get('nickname', '')
        amount = body_data.get('amount', 0)
        
        if not nickname or not amount:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Nickname and amount are required'}),
                'isBase64Encoded': False
            }
        
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
        cur = conn.cursor()
        
        cur.execute(
            "INSERT INTO donation_requests (nickname, amount, status) VALUES (%s, %s, 'pending') RETURNING id",
            (nickname, amount)
        )
        request_id = cur.fetchone()[0]
        conn.commit()
        
        bot_token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
        admin_chat_id = os.environ.get('TELEGRAM_ADMIN_CHAT_ID', '')
        
        print(f"Bot token present: {bool(bot_token)}, Admin chat ID: {admin_chat_id}")
        
        if bot_token and admin_chat_id:
            message_text = f"🔔 Новая заявка на донат!\n\n👤 Ник: {nickname}\n💰 Сумма: {amount} донат рублей\n🆔 ID заявки: {request_id}"
            
            keyboard = {
                "inline_keyboard": [[
                    {"text": "✅ Оплатил", "callback_data": f"paid_{request_id}"},
                    {"text": "❌ Не оплатил", "callback_data": f"unpaid_{request_id}"}
                ]]
            }
            
            telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            print(f"Sending to Telegram: {telegram_url[:50]}...")
            
            try:
                telegram_response = requests.post(telegram_url, json={
                    'chat_id': admin_chat_id,
                    'text': message_text,
                    'reply_markup': keyboard
                }, timeout=10)
                
                print(f"Telegram response status: {telegram_response.status_code}")
                print(f"Telegram response: {telegram_response.text}")
                
                if telegram_response.status_code == 200:
                    message_id = telegram_response.json()['result']['message_id']
                    cur.execute(
                        "UPDATE donation_requests SET telegram_message_id = %s WHERE id = %s",
                        (str(message_id), request_id)
                    )
                    conn.commit()
                    print(f"Message sent successfully, message_id: {message_id}")
                else:
                    print(f"Failed to send Telegram message: {telegram_response.text}")
            except Exception as e:
                print(f"Error sending Telegram message: {str(e)}")
        else:
            print("Telegram credentials not configured")
        
        cur.close()
        conn.close()
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'success': True, 'request_id': request_id}),
            'isBase64Encoded': False
        }
    
    if method == 'PUT':
        body_data = json.loads(event.get('body', '{}'))
        request_id = body_data.get('request_id', 0)
        new_status = body_data.get('status', 'paid')
        
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
        cur = conn.cursor()
        
        cur.execute(
            "UPDATE donation_requests SET status = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
            (new_status, request_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'success': True}),
            'isBase64Encoded': False
        }
    
    return {
        'statusCode': 405,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'error': 'Method not allowed'}),
        'isBase64Encoded': False
    }