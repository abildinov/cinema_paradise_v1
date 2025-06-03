const CACHE_NAME = 'cinema-paradise-v1.0';
const urlsToCache = [
  '/',
  '/index.html',
  '/manifest.json',
  '/icon-192.png',
  '/icon-512.png'
];

// Установка Service Worker
self.addEventListener('install', event => {
  console.log('🔧 Service Worker: Установка');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('✅ Service Worker: Кэш открыт');
        return cache.addAll(urlsToCache);
      })
      .catch(err => {
        console.log('❌ Service Worker: Ошибка кэширования', err);
      })
  );
});

// Активация Service Worker
self.addEventListener('activate', event => {
  console.log('🚀 Service Worker: Активация');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('🗑️ Service Worker: Удаление старого кэша', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Перехват запросов
self.addEventListener('fetch', event => {
  // Проверяем, что это HTTP/HTTPS запрос
  if (!event.request.url.startsWith('http')) {
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Возвращаем кэшированную версию или делаем сетевой запрос
        if (response) {
          console.log('📦 Service Worker: Загрузка из кэша', event.request.url);
          return response;
        }

        // Клонируем запрос для кэширования
        const fetchRequest = event.request.clone();

        return fetch(fetchRequest).then(response => {
          // Проверяем валидность ответа
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
          }

          // Клонируем ответ для кэширования
          const responseToCache = response.clone();

          caches.open(CACHE_NAME)
            .then(cache => {
              // Кэшируем только GET запросы
              if (event.request.method === 'GET') {
                cache.put(event.request, responseToCache);
                console.log('💾 Service Worker: Добавлено в кэш', event.request.url);
              }
            });

          return response;
        }).catch(err => {
          console.log('❌ Service Worker: Сетевая ошибка', err);
          
          // Возвращаем офлайн-страницу для навигационных запросов
          if (event.request.destination === 'document') {
            return caches.match('/');
          }
          
          // Или пустой ответ для других запросов
          return new Response('Нет подключения к интернету', {
            status: 503,
            statusText: 'Service Unavailable',
            headers: new Headers({
              'Content-Type': 'text/plain'
            })
          });
        });
      })
  );
});

// Обработка push-уведомлений
self.addEventListener('push', event => {
  console.log('📱 Service Worker: Push уведомление получено');
  
  const options = {
    body: event.data ? event.data.text() : 'Новое уведомление от Cinema Paradise',
    icon: '/icon-192.png',
    badge: '/icon-72.png',
    vibrate: [200, 100, 200],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'Открыть приложение',
        icon: '/icon-192.png'
      },
      {
        action: 'close',
        title: 'Закрыть',
        icon: '/icon-192.png'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification('🎬 Cinema Paradise', options)
  );
});

// Обработка кликов по уведомлениям
self.addEventListener('notificationclick', event => {
  console.log('🔔 Service Worker: Клик по уведомлению', event);
  
  event.notification.close();

  if (event.action === 'explore') {
    // Открываем или фокусируем окно приложения
    event.waitUntil(
      clients.matchAll().then(clientsList => {
        for (const client of clientsList) {
          if (client.url === '/' && 'focus' in client) {
            return client.focus();
          }
        }
        if (clients.openWindow) {
          return clients.openWindow('/');
        }
      })
    );
  }
});

// Обработка сообщений от приложения
self.addEventListener('message', event => {
  console.log('💬 Service Worker: Сообщение получено', event.data);
  
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

// Синхронизация в фоне
self.addEventListener('sync', event => {
  console.log('🔄 Service Worker: Фоновая синхронизация', event.tag);
  
  if (event.tag === 'background-sync') {
    event.waitUntil(doBackgroundSync());
  }
});

async function doBackgroundSync() {
  try {
    // Здесь можно синхронизировать данные с сервером
    console.log('📡 Service Worker: Выполнение фоновой синхронизации');
    
    // Пример: отправка отложенных запросов
    const pendingRequests = await getStoredRequests();
    for (const request of pendingRequests) {
      try {
        await fetch(request.url, request.options);
        await removeStoredRequest(request.id);
      } catch (err) {
        console.log('❌ Ошибка синхронизации запроса:', err);
      }
    }
  } catch (err) {
    console.log('❌ Ошибка фоновой синхронизации:', err);
  }
}

// Вспомогательные функции для работы с IndexedDB
async function getStoredRequests() {
  // Реализация получения сохраненных запросов из IndexedDB
  return [];
}

async function removeStoredRequest(id) {
  // Реализация удаления запроса из IndexedDB
  console.log('🗑️ Удален запрос:', id);
} 