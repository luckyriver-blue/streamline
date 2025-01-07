#送信後最下部へスクロールするJavascript
scroll_js = '''
<script>
    var sendButton = parent.document.querySelector('button[data-testid="stBaseButton-secondary"]');
    if (sendButton) {
        // ボタンのクリックイベントを監視
        sendButton.addEventListener('click', function() {
            // スクロール対象の要素を取得
            var target = parent.document.querySelector('section.st-emotion-cache-bm2z3a');

            if (target) {
                // スクロールを最下部に移動
                target.scrollTop = target.scrollHeight;
            } else {
                console.error("スクロール対象が見つかりません");
            }
        });
    } 
</script>
'''