function isIOS() {
  const browserInfo = navigator.userAgent.toLowerCase();
  if (browserInfo.match('iphone') || browserInfo.match('ipad')) return true;
  if (['iPad Simulator', 'iPhone Simulator', 'iPod Simulator', 'iPad', 'iPhone', 'iPod'].includes(navigator.platform)) return true;
  return false;
}

export function notify(title: string | null, options: NotificationOptions | undefined) {
    if (isIOS()) return;

    // Let's check whether notification permissions have already been granted
    if (title && Notification.permission === "granted") {
        // If it's okay let's create a notification
        const notification = new Notification(title, options);
        notification.onclick = () => window.focus();

    // Otherwise, we need to ask the user for permission
    } else if (Notification.permission !== "denied") {
        Notification.requestPermission().then(function (permission) {
            // If the user accepts, let's create a notification
            if (title && permission === "granted") {
                const notification = new Notification(title, options);
                notification.onclick = () => window.focus();
            }
        });
    }
}
