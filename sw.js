// This file runs in the background to handle push notifications

self.addEventListener('push', function(event) {
    console.log('[Service Worker] Push Received.');
    
    let data = { title: 'New Notification', body: 'Something happened!' };
    
    if (event.data) {
      try {
        data = event.data.json();
      } catch(e) {
        data = { title: 'Campus Connect', body: event.data.text() };
      }
    }
  
    const title = data.title || 'Campus Connect Alert';
    const options = {
      body: data.body || 'An item update is available.',
      icon: 'https://cdn-icons-png.flaticon.com/512/3079/3079259.png', // Optional: Generic notification icon
      badge: 'https://cdn-icons-png.flaticon.com/512/3079/3079259.png', // Optional: Generic badge
      requireInteraction: true // Keeps the notification visible until clicked
    };
  
    event.waitUntil(self.registration.showNotification(title, options));
  });
  
  self.addEventListener('notificationclick', function(event) {
    console.log('[Service Worker] Notification click Received.');
    event.notification.close();
  
    event.waitUntil(
      clients.openWindow('https://dt-prototype-a5373.web.app/dashboard') // Opens your app when clicked
    );
  });