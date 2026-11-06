<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>조간 브리핑 작성기</title>
    <style>
        :root { --primary: #0056b3; --bg: #f8f9fc; --border: #e3e6f0; }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: sans-serif; background: var(--bg); padding-bottom: 50px; }
        header { position: sticky; top: 0; background: #fff; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        header h1 { font-size: 1.2rem; color: var(--primary); }
        .btn-group { display: flex; gap: 8px; }
        button { padding: 8px 12px; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; color: #fff; }
        .btn-primary { background: var(--primary); }
        .btn-secondary { background: #6c757d; }
        .btn-success { background: #1cc88a; }
        .btn-info { background: #36b9cc; }
        .btn-del { background: #e74a3b; padding: 4px 8px; flex-shrink: 0; }
        .container { max-width: 1000px; margin: 20px auto; padding: 0 15px; }
        .card { background: #fff; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin-bottom: 20px; }
        .card-header { font-size: 1.1rem; font-weight: bold; color: var(--primary); border-bottom: 2px solid var(--border); padding-bottom: 8px; margin-bottom: 15px; display: flex; justify-content: space-between; }
        .form-group { margin-bottom: 12px; }
        label { display: block; font-weight: bold; margin-bottom: 4px; font-size: 0.9rem; }
        input[type="text"], input[type="date"], input[type="url"], textarea, select { width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; font-size: 0.9rem; }
        textarea { resize: vertical; min-height: 60px; }
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
        .input-row { display: flex; gap: 8px; margin-bottom: 8px; align-items: center; }
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 2000; justify-content: center; align-items: center; }
        .modal-content { background: #fff; width: 85%; max-width: 800px; max-height: 80vh; border-radius: 8px; overflow-y: auto; padding: 25px; position: relative; }
        .close-btn { position: absolute; top: 12px; right: 18px; font-size: 1.4rem; cursor: pointer; }
        .preview-section { margin-bottom: 18px; }
        .preview-title { font-weight: bold; background: #edf2f7; padding: 6px 10px; border-left: 4px solid var(--primary); margin-bottom: 8px; }
        .img-preview { max-width: 100%; max-height: 200px; margin-top: 8px; border: 1px dashed #ccc; padding: 4px; }
    </style>
</head>
<body>
    <header>
        <h1>📰 조간 브리핑 통합 작성기</h1>
        <div class="btn-group">
            <button class="btn-secondary" onclick="saveJSON()">작업 저장 (JSON)</button>
            <button class="btn-info" onclick="document.getElementById('jsonInput').click()">작업 불러오기</button>
            <input type="file" id="jsonInput" accept=".json" style="display:none" onchange="loadJSON(event)">
            <button class="btn-success" onclick="openPreview()">미리보기 (Run)</button>
        </div>
    </header>

    <div class="container">
        <div class="card">
            <div class="card-header">기본 정보</div>
            <div class="grid-2">
                <div class="form-group"><label>작성 일자</label><input type="date" id="briefingDate"></div>
                <div class="form-group"><label>작성자/부서</label><input type="text" id="briefingAuthor" placeholder="홍길동"></div>
            </div>
        </div>
        <div class="card">
            <div class="card-header">1. 주요 도정 키워드 & 워드클라우드 <button class="btn-secondary" onclick="addKeywordRow()">+ 추가</button></div>
            <div class="grid-2">
                <div><label>키워드 목록</label><div id="keywordContainer"></div></div>
                <div><label>워드클라우드 이미지</label><input type="file" accept="image/*" onchange="handleImageUpload(event)"><img id="wordcloudPreview" class="img-preview" style="display:none;"></div>
            </div>
        </div>
        <div class="card">
            <div class="card-header">2. 주요 방송보도 목록 <button class="btn-secondary" onclick="addBroadcastRow()">+ 추가</button></div>
            <div id="broadcastContainer"></div>
        </div>
        <div class="card">
            <div class="card-header">3. 주요 일간지 1면 헤드라인 <button class="btn-secondary" onclick="addHeadlineRow()">+ 추가</button></div>
            <div id="headlineContainer"></div>
        </div>
        <div class="card">
            <div class="card-header">4. 주요 언론 동향 <button class="btn-secondary" onclick="addTrendRow()">+ 추가</button></div>
            <div id="trendContainer"></div>
        </div>
        <div class="card">
            <div class="card-header">5. 인사 및 부고 소식 <button class="btn-secondary" onclick="addNoticeRow()">+ 추가</button></div>
            <div id="noticeContainer"></div>
        </div>
    </div>

    <div id="previewModal" class="modal">
        <div class="modal-content">
            <span class="close-btn" onclick="closePreview()">&times;</span>
            <h2 style="text-align: center; margin-bottom: 15px; color: var(--primary);">[ 미리보기 ] 조간 브리핑</h2>
            <div id="modalBody"></div>
        </div>
    </div>

    <!-- 스크립트 연결 -->
    <script src="script.js"></script>
</body>
</html>
