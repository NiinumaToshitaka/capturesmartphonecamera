/** 動体検知結果の表示領域を更新 */
function update_motion_image_area() {
    // 動体検知結果を表示する領域
    const motion_image_area = document.getElementById("motionImage");
    // 動体検知結果画像テーブル
    const motion_image_table = document.createElement("table");
    motion_image_table.setAttribute("border", "1");
    let header_row = motion_image_table.insertRow(-1);
    let table_header = document.createElement("th");
    table_header.innerText = "前フレーム";
    header_row.appendChild(table_header);
    table_header = document.createElement("th");
    table_header.innerText = "現フレーム";
    header_row.appendChild(table_header);
    table_header = document.createElement("th");
    table_header.innerText = "動体検知結果";
    header_row.appendChild(table_header);

    // 生成したテーブルをhtml要素として追加
    motion_image_area.appendChild(motion_image_table);
}

update_motion_image_area();
