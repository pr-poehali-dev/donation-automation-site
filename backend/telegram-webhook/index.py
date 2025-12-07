import json
import os
import psycopg2
import requests
from typing import Dict, Any

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    '''
    Обрабатывает callback от Telegram бота при нажатии кнопок "Оплатил" / "Не оплатил"
    Args: event - dict с httpMethod, body
          context - объект с атрибутами request_id, function_name
    Returns: HTTP response dict
    '''
    method: str = event.get('httpMethod', 'POST')
    
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Max-Age': '86400'
            },
            'body': '',
            'isBase64Encoded': False
        }
    
    if method == 'POST':
        body_data = json.loads(event.get('body', '{}'))
        
        if 'callback_query' not in body_data:
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'ok': True}),
                'isBase64Encoded': False
            }
        
        callback_data = body_data['callback_query']['data']
        message_id = body_data['callback_query']['message']['message_id']
        chat_id = body_data['callback_query']['message']['chat']['id']
        
        action, request_id = callback_data.split('_')
        new_status = 'paid' if action == 'paid' else 'rejected'
        
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
        cur = conn.cursor()
        
        cur.execute(
            "UPDATE donation_requests SET status = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s RETURNING nickname, amount",
            (new_status, int(request_id))
        )
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        if result:
            nickname, amount = result
            status_text = "✅ ОПЛАЧЕНО" if new_status == 'paid' else "❌ ОТКЛОНЕНО"
            new_message = f"{status_text}\n\n👤 Ник: {nickname}\n💰 Сумма: {amount} донат рублей\n🆔 ID заявки: {request_id}"
            
            bot_token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
            
            edit_url = f"https://api.telegram.org/bot{bot_token}/editMessageText"
            requests.post(edit_url, json={
                'chat_id': chat_id,
                'message_id': message_id,
                'text': new_message
            })
            
            answer_url = f"https://api.telegram.org/bot{bot_token}/answerCallbackQuery"
            requests.post(answer_url, json={
                'callback_query_id': body_data['callback_query']['id'],
                'text': f'Статус обновлён: {status_text}'
            })
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'ok': True}),
            'isBase64Encoded': False
        }
    
    return {
        'statusCode': 405,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'error': 'Method not allowed'}),
        'isBase64Encoded': False
    }
