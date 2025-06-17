import asyncio
from datetime import datetime
from aiohttp import web
import aiohttp_cors

# Хранилище объявлений в памяти
advertisements = {}
current_id = 1

# === Роуты ===

async def create_advertisement(request):
    """Создание нового объявления"""
    try:
        data = await request.json()
    except Exception:
        return web.json_response({'error': 'Invalid JSON'}, status=400)

    # Валидация обязательных полей
    if not data or 'title' not in data or 'author' not in data:
        return web.json_response({'error': 'Title and author are required'}, status=404)

    global current_id
    ad = {
        'id': current_id,
        'title': data['title'],
        'description': data.get('description', ''),
        'price': float(data.get('price', 0)),
        'author': data['author'],
        'created_at': datetime.now().isoformat()
    }

    advertisements[current_id] = ad
    current_id += 1

    return web.json_response(ad, status=201)


async def get_advertisement(request):
    """Получение объявления по ID"""
    ad_id = int(request.match_info['ad_id'])
    if ad_id not in advertisements:
        return web.json_response({'error': 'Advertisement not found'}, status=404)

    return web.json_response(advertisements[ad_id])


async def update_advertisement(request):
    """Обновление объявления"""
    ad_id = int(request.match_info['ad_id'])
    if ad_id not in advertisements:
        return web.json_response({'error': 'Advertisement not found'}, status=404)

    try:
        data = await request.json()
    except Exception:
        return web.json_response({'error': 'Invalid JSON'}, status=400)

    ad = advertisements[ad_id]

    # Обновляем только те поля, которые пришли в запросе
    if 'title' in data:
        ad['title'] = data['title']
    if 'description' in data:
        ad['description'] = data['description']
    if 'price' in data:
        ad['price'] = float(data['price'])
    if 'author' in data:
        ad['author'] = data['author']

    return web.json_response(ad)


async def delete_advertisement(request):
    """Удаление объявления"""
    ad_id = int(request.match_info['ad_id'])
    if ad_id not in advertisements:
        return web.json_response({'error': 'Advertisement not found'}, status=404)

    del advertisements[ad_id]
    return web.json_response({'message': 'Advertisement deleted successfully'})


async def search_advertisements(request):
    """Поиск объявлений по параметрам"""
    title = request.query.get('title')
    author = request.query.get('author')
    price_min = float(request.query.get('price_min')) if request.query.get('price_min') else None
    price_max = float(request.query.get('price_max')) if request.query.get('price_max') else None

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

    return web.json_response(results)

# === Запуск приложения ===

def init_app():
    app = web.Application()

    # Настройка CORS
    cors = aiohttp_cors.setup(app)

    resource_options = aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers=["Content-Type"]
    )

    # Явно создаём ресурсы (Resource) для каждого маршрута
    resource_ads = app.router.add_resource('/advertisements')
    route_ads = resource_ads.add_route('POST', create_advertisement)
    cors.add(route_ads, {"*": resource_options})

    resource_ad_id = app.router.add_resource('/advertisements/{ad_id}')
    cors.add(resource_ad_id.add_route('GET', get_advertisement), {"*": resource_options})
    cors.add(resource_ad_id.add_route('PUT', update_advertisement), {"*": resource_options})
    cors.add(resource_ad_id.add_route('DELETE', delete_advertisement), {"*": resource_options})

    resource_search = app.router.add_resource('/advertisements')
    cors.add(resource_search.add_route('GET', search_advertisements), {"*": resource_options})

    return app


if __name__ == '__main__':
    app = init_app()
    web.run_app(app, host='0.0.0.0', port=8000)