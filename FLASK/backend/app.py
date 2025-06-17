from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS  # Добавляем импорт

from typing import Dict
   


app = Flask(__name__)
CORS(app, resources={
    r"/advertisements*": {
        "origins": ["http://localhost:*", "http://frontend:*"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# ... остальной код бэкенда без изменений ...

# Хранилище объявлений в памяти (в реальном приложении нужно использовать БД)
advertisements: Dict[int, dict] = {}
current_id = 1

@app.route('/advertisements', methods=['POST'])
def create_advertisement():
    """Создание нового объявления"""
    global current_id
    
    data = request.get_json()
    
    # Валидация обязательных полей
    if not data or 'title' not in data or 'author' not in data:
        return jsonify({'error': 'Title and author are required'}), 400
    
    # Создание объявления
    ad = {
        'id': current_id,
        'title': data['title'],
        'description': data.get('description', ''),
        'price': data.get('price', 0),
        'author': data['author'],
        'created_at': datetime.now().isoformat()
    }
    
    advertisements[current_id] = ad
    current_id += 1
    
    return jsonify(ad), 201

@app.route('/advertisements/<int:ad_id>', methods=['GET'])
def get_advertisement(ad_id):
    """Получение объявления по ID"""
    if ad_id not in advertisements:
        return jsonify({'error': 'Advertisement not found'}), 404
    
    return jsonify(advertisements[ad_id])

@app.route('/advertisements/<int:ad_id>', methods=['PUT'])
def update_advertisement(ad_id):
    """Обновление объявления"""
    if ad_id not in advertisements:
        return jsonify({'error': 'Advertisement not found'}), 404
    
    data = request.get_json()
    ad = advertisements[ad_id]
    
    # Обновляем только те поля, которые пришли в запросе
    if 'title' in data:
        ad['title'] = data['title']
    if 'description' in data:
        ad['description'] = data['description']
    if 'price' in data:
        ad['price'] = data['price']
    if 'author' in data:
        ad['author'] = data['author']
    
    return jsonify(ad)

@app.route('/advertisements/<int:ad_id>', methods=['DELETE'])
def delete_advertisement(ad_id):
    """Удаление объявления"""
    if ad_id not in advertisements:
        return jsonify({'error': 'Advertisement not found'}), 404
    
    del advertisements[ad_id]
    return jsonify({'message': 'Advertisement deleted successfully'}), 200

@app.route('/advertisements', methods=['GET'])
def search_advertisements():
    """Поиск объявлений по параметрам"""
    title = request.args.get('title')
    author = request.args.get('author')
    price_min = request.args.get('price_min', type=float)
    price_max = request.args.get('price_max', type=float)
    
    results = []
    
    for ad in advertisements.values():
        # Фильтрация по заголовку
        if title and title.lower() not in ad['title'].lower():
            continue
            
        # Фильтрация по автору
        if author and author.lower() not in ad['author'].lower():
            continue
            
        # Фильтрация по цене
        if price_min is not None and ad['price'] < price_min:
            continue
        if price_max is not None and ad['price'] > price_max:
            continue
            
        results.append(ad)
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)