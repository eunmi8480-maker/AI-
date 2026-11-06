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
    const div = document.createElement('div');
    div.className = 'input-row';
    div.innerHTML = `<input type="text" class="keyword-input" value="${val}" placeholder="키워드 입력"><button class="btn-del" onclick="this.parentElement.remove()">삭제</button>`;
    document.getElementById('keywordContainer').appendChild(div);
}

function addBroadcastRow(media = '', title = '', url = '') {
    const div = document.createElement('div');
    div.className = 'input-row';
    div.innerHTML = `<input type="text" class="bc-media" style="width:20%" value="${media}" placeholder="방송사"><input type="text" class="bc-title" style="width:50%" value="${title}" placeholder="제목"><input type="url" class="bc-url" style="width:30%" value="${url}" placeholder="URL"><button class="btn-del" onclick="this.parentElement.remove()">삭제</button>`;
    document.getElementById('broadcastContainer').appendChild(div);
}

function addHeadlineRow(press = '', headline = '') {
    const div = document.createElement('div');
    div.className = 'input-row';
    div.innerHTML = `<input type="text" class="hl-press" style="width:25%" value="${press}" placeholder="신문사"><input type="text" class="hl-title" style="width:75%" value="${headline}" placeholder="1면 헤드라인"><button class="btn-del" onclick="this.parentElement.remove()">삭제</button>`;
    document.getElementById('headlineContainer').appendChild(div);
}

function addTrendRow(category = '', text = '') {
    const div = document.createElement('div');
    div.className = 'input-row';
    div.innerHTML = `<input type="text" class="tr-cat" style="width:20%" value="${category}" placeholder="구분"><textarea class="tr-text" style="width:80%" placeholder="동향 내용">${text}</textarea><button class="btn-del" onclick="this.parentElement.remove()">삭제</button>`;
    document.getElementById('trendContainer').appendChild(div);
}

function addNoticeRow(type = '인사', content = '') {
    const div = document.createElement('div');
    div.className = 'input-row';
    div.innerHTML = `<select class="nt-type" style="width:20%"><option value="인사" ${type==='인사'?'selected':''}>인사</option><option value="부고" ${type==='부고'?'selected':''}>부고</option><option value="동정" ${type==='동정'?'selected':''}>동정</option></select><input type="text" class="nt-content" style="width:80%" value="${content}" placeholder="내용 입력"><button class="btn-del" onclick="this.parentElement.remove()">삭제</button>`;
    document.getElementById('noticeContainer').appendChild(div);
}

function handleImageUpload(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(evt) {
            wordcloudBase64 = evt.target.result;
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
        })).filter(i => i.title),
        headlines: Array.from(document.querySelectorAll('#headlineContainer .input-row')).map(row => ({
            press: row.querySelector('.hl-press').value,
            title: row.querySelector('.hl-title').value
        })).filter(i => i.title),
        trends: Array.from(document.querySelectorAll('#trendContainer .input-row')).map(row => ({
            category: row.querySelector('.tr-cat').value,
            text: row.querySelector('.tr-text').value
        })).filter(i => i.text),
        notices: Array.from(document.querySelectorAll('#noticeContainer .input-row')).map(row => ({
            type: row.querySelector('.nt-type').value,
            content: row.querySelector('.nt-content').value
        })).filter(i => i.content)
    };
}

function openPreview() {
    const d = getFormData();
    let html = `<div style="text-align:right; color:#666; font-size:0.9rem; margin-bottom:10px;">일자: ${d.date} | 작성자: ${d.author || '미지정'}</div>`;
    
    html += `<div class="preview-section"><div class="preview-title">1. 주요 도정 키워드</div><p><strong>키워드:</strong> ${d.keywords.join(', ') || '없음'}</p>${d.wordcloud ? `<img src="${d.wordcloud}" style="max-width:100%; border:1px solid #ddd; margin-top:8px;">` : ''}</div>`;
    html += `<div class="preview-section"><div class="preview-title">2. 방송보도</div><ul>${d.broadcasts.map(b => `<li>[${b.media}] ${b.title} ${b.url ? `<a href="${b.url}" target="_blank">(링크)</a>` : ''}</li>`).join('') || '<li>없음</li>'}</ul></div>`;
    html += `<div class="preview-section"><div class="preview-title">3. 1면 헤드라인</div><ul>${d.headlines.map(h => `<li><strong>${h.press}:</strong> ${h.title}</li>`).join('') || '<li>없음</li>'}</ul></div>`;
    html += `<div class="preview-section"><div class="preview-title">4. 언론 동향</div><ul>${d.trends.map(t => `<li><strong>[${t.category}]</strong> ${t.text}</li>`).join('') || '<li>없음</li>'}</ul></div>`;
    html += `<div class="preview-section"><div class="preview-title">5. 인사 및 부고</div><ul>${d.notices.map(n => `<li><strong>[${n.type}]</strong> ${n.content}</li>`).join('') || '<li>없음</li>'}</ul></div>`;

    document.getElementById('modalBody').innerHTML = html;
    document.getElementById('previewModal').style.display = 'flex';
}

function closePreview() {
    document.getElementById('previewModal').style.display = 'none';
}

function saveJSON() {
    const data = getFormData();
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `조간브리핑_${data.date || '작성분'}.json`;
    a.click();
}

function loadJSON(e) {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function(evt) {
        try {
            const data = JSON.parse(evt.target.result);
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

            alert('불러오기 완료!');
        } catch (err) {
            alert('JSON 파일 형식이 맞지 않습니다.');
        }
    };
    reader.readAsText(file);
}