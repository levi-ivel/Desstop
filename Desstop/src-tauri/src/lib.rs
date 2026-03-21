#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_positioner::init())
        .plugin(tauri_plugin_opener::init())
        .setup(|app| {
            use tauri::Manager;
            use tauri_plugin_positioner::{Position, WindowExt};

            if let Some(window) = app.get_webview_window("main") {
                let _ = window.set_position(tauri::LogicalPosition::new(0.0, 0.0));

                let window_clone = window.clone();
                std::thread::spawn(move || {
                    std::thread::sleep(std::time::Duration::from_millis(1000));
                    
                    let _ = window_clone.set_position(tauri::LogicalPosition::new(0.0, 0.0));
                    
                    if let Ok(Some(_)) = window_clone.current_monitor() {
                        let _ = window_clone.move_window(Position::TopLeft);
                    }
                });
            }
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
