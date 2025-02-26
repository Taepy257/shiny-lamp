// map_interaction.js (JavaScript 코드 - 지도에서 영역 선택)
var map = L.map('map').setView([37.5665, 126.9780], 10); // 서울 중심
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

var rectangle = null;
var startPoint = null;

map.on('click', function (e) {
    if (!startPoint) {
        // 첫 번째 클릭 -> 시작점 저장
        startPoint = e.latlng;
    } else {
        // 두 번째 클릭 -> 직사각형 그리기
        var endPoint = e.latlng;

        // 기존 사각형 삭제
        if (rectangle) {
            map.removeLayer(rectangle);
        }

        // 직사각형 좌표 계산
        var bounds = [startPoint, endPoint];
        rectangle = L.rectangle(bounds, {color: "blue", weight: 2}).addTo(map);

        // Python으로 좌표 전달
        if (window.pyBridge) {
            window.pyBridge.sendRectangleCoords(
                startPoint.lat, startPoint.lng,
                endPoint.lat, endPoint.lng
            );
        }

        // 초기화 (다시 선택 가능)
        startPoint = null;
    }
});
