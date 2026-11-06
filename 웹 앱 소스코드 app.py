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
