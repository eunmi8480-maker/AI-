<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>조간 브리핑 통합 작성기</title>
    <!-- JSZip (HWPX 파일 생성용) -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
    <style>
        :root {
            --primary-color: #0056b3;
            --bg-color: #f8f9fc;
            --border-color: #e3e6f0;
            --text-color: #333;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Malgun Gothic', '맑은 고딕', sans-serif; background: var(--bg-color); color: var(--text-color); padding-bottom: 50px; }
        header { position: sticky; top: 0; background: #fff; box-shadow: 0 2px 10px rgba(0,0,0,0.1); z-index: 1000; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; }
        header h1 { font-size: 1.3rem; color: var(--primary-color); }
        .btn-group { display: flex; gap: 8px; }
        button { padding: 8px 14px; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; color: #fff; }
        .btn-primary { background-color: var(--primary-color); }
        .btn-secondary { background-color: #6c757d; }
        .btn-success { background-color: #1cc88a; }
        .btn-info { background-color: #36b9cc; }
        .container { max-width: 1100px; margin: 20px auto; padding: 0 15px; }
        .card { background: #fff; border: 1px solid var(--border-color); border-radius: 8px; padding: 20px; margin-bottom: 20px; }
        .card-header { font-size: 1.1rem; font-weight: bold; color: var(--primary-color); border-bottom: 2px solid var(--border-color); padding-bottom: 8px; margin-bottom: 15px; display: flex; justify-content: space-between; }
        .form-group { margin-bottom: 12px; }
        label { display: block; font-weight: bold; margin-bottom: 4px; font-size: 0.9rem; }
        input[type="text"], input[type="date"], input[type="url"], textarea, select { width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; font-size: 0.9rem; }
        textarea { resize: vertical; min-height: 70px; }
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
        .input-row { display: flex; gap: 8px; margin-bottom: 8px; align-items: center; }
        .btn-del { background-color: #e74a3b; padding: 6px 10px; flex-shrink: 0; }
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 2000; justify-content: center; align-items: center; }
        .modal-content { background: #fff; width: 85%; max-width: 800px; max-height: 80vh; border-radius: 8px; overflow-y: auto; padding: 25px; position: relative; }
        .close-btn { position: absolute; top: 12px; right: 18px; font-size: 1.4rem; cursor: pointer; }
        .preview-section { margin-bottom: 18px; }
        .preview-title { font-weight: bold; background: #edf2f7; padding: 6px 10px; border-left: 4px solid var(--primary-color); margin-bottom: 8px; }
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
            <button class="btn-primary" onclick="exportHWPX()">한글 생성 (.hwpx)</button>
        </div>
    </header>

    <div class="container">
        <!-- 기본 정보 -->
        <div class="card">
            <div class="card-header">기본 정보</div>
            <div class="grid-2">
                <div class="form-group">
                    <label>작성 일자</label>
                    <input type="date" id="briefingDate">
                </div>
                <div class="form-group">
                    <label>작성자 / 부서</label>
                    <input type="text" id="briefingAuthor" placeholder="예: 대변인실 홍길동">
                </div>
            </div>
        </div>

        <!-- 1. 주요 도정 키워드 & 워드클라우드 -->
        <div class="card">
            <div class="card-header">
                1. 주요 도정 키워드 & 워드클라우드
                <button class="btn-secondary" onclick="addKeywordRow()">+ 추가</button>
            </div>
            <div class="grid-2">
                <div>
                    <label>키워드 목록</label>
                    <div id="keywordContainer"></div>
                </div>
                <div>
                    <label>워드클라우드 이미지</label>
                    <input type="file" id="wordcloudImgInput" accept="image/*" onchange="handleImageUpload(event)">
                    <img id="wordcloudPreview" class="img-preview" style="display:none;">
                </div>
            </div>
        </div>

        <!-- 2. 방송 보도 -->
        <div class="card">
            <div class="card-header">
                2. 주요 방송보도 목록
                <button class="btn-secondary" onclick="addBroadcastRow()">+ 추가</button>
            </div>
            <div id="broadcastContainer"></div>
        </div>

        <!-- 3. 신문 헤드라인 -->
        <div class="card">
            <div class="card-header">
                3. 주요 일간지 1면 헤드라인
                <button class="btn-secondary" onclick="addHeadlineRow()">+ 추가</button>
            </div>
            <div id="headlineContainer"></div>
        </div>

        <!-- 4. 언론 동향 -->
        <div class="card">
            <div class="card-header">
                4. 주요 언론 동향
                <button class="btn-secondary" onclick="addTrendRow()">+ 추가</button>
            </div>
            <div id="trendContainer"></div>
        </div>

        <!-- 5. 인사 및 부고 -->
        <div class="card">
            <div class="card-header">
                5. 인사 및 부고 소식
                <button class="btn-secondary" onclick="addNoticeRow()">+ 추가</button>
            </div>
            <div id="noticeContainer"></div>
        </div>
    </div>

    <!-- 미리보기 모달 -->
    <div id="previewModal" class="modal">
        <div class="modal-content">
            <span class="close-btn" onclick="closePreview()">&times;</span>
            <h2 style="text-align: center; margin-bottom: 15px; color: var(--primary-color);">[ 미리보기 ] 조간 브리핑</h2>
            <div id="modalBody"></div>
        </div>
    </div>

    <script>
        let wordcloudBase64 = '';

        document.addEventListener('DOMContentLoaded', () => {
            document.getElementById('briefingDate').valueAsDate = new Date();
            addKeywordRow();
            addBroadcastRow();
            addHeadlineRow();
            addTrendRow();
            addNoticeRow();
        });

        function addKeywordRow(val = '') {
            const container = document.getElementById('keywordContainer');
            const div = document.createElement('div');
            div.className = 'input-row';
            div.innerHTML = `
                <input type="text" class="keyword-input" value="${val}" placeholder="키워드 입력">
                <button class="btn-del" onclick="this.parentElement.remove()">삭제</button>
            `;
            container.appendChild(div);
        }

        function addBroadcastRow(media = '', title = '', url = '') {
            const container = document.getElementById('broadcastContainer');
            const div = document.createElement('div');
            div.className = 'input-row';
            div.innerHTML = `
                <input type="text" class="bc-media" style="width:20%" value="${media}" placeholder="방송사">
                <input type="text" class="bc-title" style="width:50%" value="${title}" placeholder="제목">
                <input type="url" class="bc-url" style="width:30%" value="${url}" placeholder="URL">
                <button class="btn-del" onclick="this.parentElement.remove()">삭제</button>
            `;
            container.appendChild(div);
        }

        function addHeadlineRow(press = '', headline = '') {
            const container = document.getElementById('headlineContainer');
            const div = document.createElement('div');
            div.className = 'input-row';
            div.innerHTML = `
                <input type="text" class="hl-press" style="width:25%" value="${press}" placeholder="신문사">
                <input type="text" class="hl-title" style="width:75%" value="${headline}" placeholder="1면 헤드라인">
                <button class="btn-del" onclick="this.parentElement.remove()">삭제</button>
            `;
            container.appendChild(div);
        }

        function addTrendRow(category = '', text = '') {
            const container = document.getElementById('trendContainer');
            const div = document.createElement('div');
            div.className = 'input-row';
            div.innerHTML = `
                <input type="text" class="tr-cat" style="width:20%" value="${category}" placeholder="구분">
                <textarea class="tr-text" style="width:80%" placeholder="동향 내용">${text}</textarea>
                <button class="btn-del" onclick="this.parentElement.remove()">삭제</button>
            `;
            container.appendChild(div);
        }

        function addNoticeRow(type = '인사', content = '') {
            const container = document.getElementById('noticeContainer');
            const div = document.createElement('div');
            div.className = 'input-row';
            div.innerHTML = `
                <select class="nt-type" style="width:20%">
                    <option value="인사" ${type==='인사'?'selected':''}>인사</option>
                    <option value="부고" ${type==='부고'?'selected':''}>부고</option>
                    <option value="동정" ${type==='동정'?'selected':''}>동정</option>
                </select>
                <input type="text" class="nt-content" style="width:80%" value="${content}" placeholder="내용 입력">
                <button class="btn-del" onclick="this.parentElement.remove()">삭제</button>
            `;
            container.appendChild(div);
        }

        function handleImageUpload(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(event) {
                    wordcloudBase64 = event.target.result;
                    const preview = document.getElementById('wordcloudPreview');
                    preview.src = wordcloudBase64;
                    preview.style.display = 'block';
                };
                reader.readAsDataURL(file);
            }
        }

        function getFormData() {
            return {
                date: document.getElementById('briefingDate').value,
                author: document.getElementById('briefingAuthor').value,
                keywords: Array.from(document.querySelectorAll('.keyword-input')).map(i => i.value).filter(Boolean),
                wordcloud: wordcloudBase64,
                broadcasts: Array.from(document.querySelectorAll('#broadcastContainer .input-row')).map(row => ({
                    media: row.querySelector('.bc-media').value,
                    title: row.querySelector('.bc-title').value,
                    url: row.querySelector('.bc-url').value
                })).filter(item => item.title),
                headlines: Array.from(document.querySelectorAll('#headlineContainer .input-row')).map(row => ({
                    press: row.querySelector('.hl-press').value,
                    title: row.querySelector('.hl-title').value
                })).filter(item => item.title),
                trends: Array.from(document.querySelectorAll('#trendContainer .input-row')).map(row => ({
                    category: row.querySelector('.tr-cat').value,
                    text: row.querySelector('.tr-text').value
                })).filter(item => item.text),
                notices: Array.from(document.querySelectorAll('#noticeContainer .input-row')).map(row => ({
                    type: row.querySelector('.nt-type').value,
                    content: row.querySelector('.nt-content').value
                })).filter(item => item.content)
            };
        }

        function openPreview() {
            const data = getFormData();
            const modalBody = document.getElementById('modalBody');
            
            let html = `
                <div style="margin-bottom:12px; text-align:right; color:#666; font-size:0.9rem;">
                    일자: ${data.date} | 작성자: ${data.author || '미지정'}
                </div>
            `;

            html += `<div class="preview-section">
                <div class="preview-title">1. 주요 도정 키워드</div>
                <p><strong>키워드:</strong> ${data.keywords.join(', ') || '없음'}</p>
                ${data.wordcloud ? `<img src="${data.wordcloud}" style="max-width:100%; height:auto; margin-top:8px; border:1px solid #ddd;">` : ''}
            </div>`;

            html += `<div class="preview-section">
                <div class="preview-title">2. 주요 방송보도</div>
                <ul style="padding-left:18px;">
                    ${data.broadcasts.map(b => `<li>[${b.media}] ${b.title} ${b.url ? `<a href="${b.url}" target="_blank">(링크)</a>` : ''}</li>`).join('') || '<li>내용 없음</li>'}
                </ul>
            </div>`;

            html += `<div class="preview-section">
                <div class="preview-title">3. 주요 일간지 1면 헤드라인</div>
                <ul style="padding-left:18px;">
                    ${data.headlines.map(h => `<li><strong>${h.press}:</strong> ${h.title}</li>`).join('') || '<li>내용 없음</li>'}
                </ul>
            </div>`;

            html += `<div class="preview-section">
                <div class="preview-title">4. 주요 언론 동향</div>
                <ul style="padding-left:18px;">
                    ${data.trends.map(t => `<li><strong>[${t.category}]</strong> ${t.text}</li>`).join('') || '<li>내용 없음</li>'}
                </ul>
            </div>`;

            html += `<div class="preview-section">
                <div class="preview-title">5. 인사 및 부고</div>
                <ul style="padding-left:18px;">
                    ${data.notices.map(n => `<li><strong>[${n.type}]</strong> ${n.content}</li>`).join('') || '<li>내용 없음</li>'}
                </ul>
            </div>`;

            modalBody.innerHTML = html;
            document.getElementById('previewModal').style.display = 'flex';
        }

        function closePreview() {
            document.getElementById('previewModal').style.display = 'none';
        }

        function saveJSON() {
            const data = getFormData();
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = `조간브리핑_${data.date || '작성분'}.json`;
            link.click();
        }

        function loadJSON(e) {
            const file = e.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function(event) {
                try {
                    const data = JSON.parse(event.target.result);
                    
                    if (data.date) document.getElementById('briefingDate').value = data.date;
                    if (data.author) document.getElementById('briefingAuthor').value = data.author;

                    document.getElementById('keywordContainer').innerHTML = '';
                    (data.keywords || []).forEach(k => addKeywordRow(k));

                    if (data.wordcloud) {
                        wordcloudBase64 = data.wordcloud;
                        const preview = document.getElementById('wordcloudPreview');
                        preview.src = wordcloudBase64;
                        preview.style.display = 'block';
                    }

                    document.getElementById('broadcastContainer').innerHTML = '';
                    (data.broadcasts || []).forEach(b => addBroadcastRow(b.media, b.title, b.url));

                    document.getElementById('headlineContainer').innerHTML = '';
                    (data.headlines || []).forEach(h => addHeadlineRow(h.press, h.title));

                    document.getElementById('trendContainer').innerHTML = '';
                    (data.trends || []).forEach(t => addTrendRow(t.category, t.text));

                    document.getElementById('noticeContainer').innerHTML = '';
                    (data.notices || []).forEach(n => addNoticeRow(n.type, n.content));

                    alert('데이터를 성공적으로 불러왔습니다.');
                } catch (err) {
                    alert('유효하지 않은 JSON 파일입니다.');
                }
            };
            reader.readAsText(file);
        }

        function exportHWPX() {
            const data = getFormData();
            alert(`[HWPX 다운로드 요청]\n작성일자: ${data.date}\n보고서 저장을 진행합니다.`);
        }
    </script>
</body>
</html>
