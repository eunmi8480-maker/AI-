<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>조간 브리핑 통합 작성기</title>
    <!-- JSZip 라이브러리 (HWPX 압축 및 생성용) -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
    <style>
        :root {
            --primary-color: #0056b3;
            --secondary-color: #4e73df;
            --bg-color: #f8f9fc;
            --border-color: #e3e6f0;
            --text-color: #333;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Malgun Gothic', '맑은 고딕', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            line-height: 1.5;
            padding-bottom: 50px;
        }

        /* Top Fixed Navigation */
        header {
            position: sticky;
            top: 0;
            background-color: #ffffff;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        header h1 {
            font-size: 1.4rem;
            color: var(--primary-color);
        }

        .btn-group {
            display: flex;
            gap: 10px;
        }

        button {
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.2s ease;
        }

        .btn-primary { background-color: var(--primary-color); color: #fff; }
        .btn-primary:hover { background-color: #003d80; }
        .btn-secondary { background-color: #6c757d; color: #fff; }
        .btn-secondary:hover { background-color: #5a6268; }
        .btn-success { background-color: #1cc88a; color: #fff; }
        .btn-success:hover { background-color: #17a673; }
        .btn-info { background-color: #36b9cc; color: #fff; }
        .btn-info:hover { background-color: #2c9faf; }

        /* Container & Cards */
        .container {
            max-width: 1200px;
            margin: 30px auto;
            padding: 0 20px;
        }
