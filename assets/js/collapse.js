$(".header").click(function () {

    $header = $(this);
    // 获取下一个元素
    $content = $header.next();
    // 切换内容区域展开/收起：可见则上滑收起，不可见则下滑展开
    $content.slideToggle(500, function () {
        // 在 slideToggle 执行完成后回调
        // 根据内容区域可见性更新标题文字
        $header.text(function () {
            // 按条件切换文案
            return $content.is(":visible") ? "Collapse" : "Expand";
        });
    });

});
