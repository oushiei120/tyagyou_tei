/*
 * A TEI Viewer for East Asian Pre-Modern Texts
 *
 * Written by Jun HOMMA (FLX Style)
 */
(function() {
    const config = {
        xmlidPickup: [
            // selectorは必須、labelは任意（未設定の場合selectorを使用）
            {
                selector: 'seg[type="題"]',
                label: '題'
            },
            {
                selector: 'person',
                label: '人物'
            },
            {
                selector: 'l',
                label: '和歌'
            },
            {
                selector: 'seg[type="解説"]',
                label: '解説'
            },
        ],
        typeToGraphLabelMapping: {
            'kakusen': '格箋',
            'hyosen': '平箋',
            'chisen': '智箋'
        },
        enableGraph: true,
        openSeadragon: {
            highlight: true
        }
    };
    return TEIViewer(config);
})();