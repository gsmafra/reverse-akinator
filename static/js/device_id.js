export function getDeviceId() {
    let deviceId = localStorage.getItem('deviceId');
    if (!deviceId) {
        const userAgentInfo = navigator.userAgent;
        const os = getOS(userAgentInfo);
        const browser = getBrowser(userAgentInfo);
        const randomPart = generateRandomPart();
        deviceId = `${os}-${browser}-${randomPart}`;
        localStorage.setItem('deviceId', deviceId);
    }
    return deviceId;
}

function generateRandomPart() {
    return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
}

function getOS(userAgent) {
    if (userAgent.indexOf("Win") != -1) return "Windows";
    if (userAgent.indexOf("Mac") != -1) return "MacOS";
    if (userAgent.indexOf("Linux") != -1) return "Linux";
    if (userAgent.indexOf("Android") != -1) return "Android";
    if (userAgent.indexOf("iOS") != -1) return "iOS";
    return "UnknownOS";
}

function getBrowser(userAgent) {
    if (userAgent.indexOf("Chrome") != -1 && userAgent.indexOf("Edg") == -1) return "Chrome";
    if (userAgent.indexOf("Firefox") != -1) return "Firefox";
    if (userAgent.indexOf("Safari") != -1 && userAgent.indexOf("Chrome") == -1) return "Safari";
    if (userAgent.indexOf("Opera") != -1 || userAgent.indexOf("OPR") != -1) return "Opera";
    if (userAgent.indexOf("Edg") != -1) return "Edge";
    if (userAgent.indexOf("Trident") != -1) return "IE";
    return "UnknownBrowser";
}
