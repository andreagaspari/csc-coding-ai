<?php
/*
Plugin Name: Simple Booking Calendar
Description: Plugin per la gestione di un sistema di booking semplice con custom post type "calendario".
Version: 1.0
Author: Il Tuo Nome
*/

// Registrazione del Custom Post Type "calendario"
function sbc_register_calendario_post_type() {
    $labels = array(
        'name' => 'Calendari',
        'singular_name' => 'Calendario',
        'menu_name' => 'Calendari',
        'name_admin_bar' => 'Calendario',
        'add_new' => 'Aggiungi Nuovo',
        'add_new_item' => 'Aggiungi Nuovo Calendario',
        'new_item' => 'Nuovo Calendario',
        'edit_item' => 'Modifica Calendario',
        'view_item' => 'Visualizza Calendario',
        'all_items' => 'Tutti i Calendari',
        'search_items' => 'Cerca Calendari',
        'not_found' => 'Nessun calendario trovato',
        'not_found_in_trash' => 'Nessun calendario trovato nel cestino',
    );

    $args = array(
        'labels' => $labels,
        'public' => true,
        'has_archive' => true,
        'rewrite' => array('slug' => 'calendario'),
        'supports' => array('title'),
        'show_in_rest' => true,
    );

    register_post_type('calendario', $args);
}
add_action('init', 'sbc_register_calendario_post_type');

// Aggiunta dei campi personalizzati: data, ora, stato prenotazione
function sbc_add_calendario_meta_boxes() {
    add_meta_box(
        'sbc_calendario_details',
        'Dettagli Prenotazione',
        'sbc_calendario_meta_box_callback',
        'calendario',
        'normal',
        'default'
    );
}
add_action('add_meta_boxes', 'sbc_add_calendario_meta_boxes');

function sbc_calendario_meta_box_callback($post) {
    $data = get_post_meta($post->ID, '_sbc_data', true);
    $ora = get_post_meta($post->ID, '_sbc_ora', true);
    $stato = get_post_meta($post->ID, '_sbc_stato', true);
    ?>
    <label for="sbc_data">Data:</label>
    <input type="date" name="sbc_data" value="<?php echo esc_attr($data); ?>" /><br><br>
    <label for="sbc_ora">Ora:</label>
    <input type="time" name="sbc_ora" value="<?php echo esc_attr($ora); ?>" /><br><br>
    <label for="sbc_stato">Stato Prenotazione:</label>
    <select name="sbc_stato">
        <option value="libero" <?php selected($stato, 'libero'); ?>>Libero</option>
        <option value="prenotato" <?php selected($stato, 'prenotato'); ?>>Prenotato</option>
    </select>
    <?php
}

function sbc_save_calendario_meta($post_id) {
    if (array_key_exists('sbc_data', $_POST)) {
        update_post_meta($post_id, '_sbc_data', sanitize_text_field($_POST['sbc_data']));
    }
    if (array_key_exists('sbc_ora', $_POST)) {
        update_post_meta($post_id, '_sbc_ora', sanitize_text_field($_POST['sbc_ora']));
    }
    if (array_key_exists('sbc_stato', $_POST)) {
        update_post_meta($post_id, '_sbc_stato', sanitize_text_field($_POST['sbc_stato']));
    }
}
add_action('save_post', 'sbc_save_calendario_meta');

// Shortcode per mostrare il calendario degli slot disponibili
function sbc_render_booking_calendar() {
    // Impostazioni calendario
    $giorni_settimana = array('Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì');
    $ora_inizio = 9;
    $ora_fine = 13;
    $slot_durata = 30; // minuti

    // Calcola la settimana corrente (lunedì-venerdì)
    $oggi = current_time('timestamp');
    $inizio_settimana = strtotime('monday this week', $oggi);
    $output = '<table class="sbc-calendar" style="border-collapse:collapse;width:100%;max-width:600px;">';
    $output .= '<thead><tr><th>Giorno</th><th>Orario</th><th>Stato</th><th>Prenota</th></tr></thead><tbody>';

    for ($g = 0; $g < 5; $g++) {
        $data_giorno = strtotime("+{$g} day", $inizio_settimana);
        $data_str = date('Y-m-d', $data_giorno);
        $giorno_nome = $giorni_settimana[$g];
        for ($ora = $ora_inizio; $ora < $ora_fine; $ora++) {
            for ($min = 0; $min < 60; $min += $slot_durata) {
                $ora_str = sprintf('%02d:%02d', $ora, $min);
                // Verifica se lo slot è prenotato
                $args = array(
                    'post_type' => 'calendario',
                    'meta_query' => array(
                        array('key' => '_sbc_data', 'value' => $data_str, 'compare' => '='),
                        array('key' => '_sbc_ora', 'value' => $ora_str, 'compare' => '='),
                        array('key' => '_sbc_stato', 'value' => 'prenotato', 'compare' => '=')
                    ),
                    'posts_per_page' => 1
                );
                $prenotato = new WP_Query($args);
                $is_prenotato = $prenotato->have_posts();
                $stato = $is_prenotato ? '<span style="color:red;">Prenotato</span>' : '<span style="color:green;">Libero</span>';
                $output .= '<tr>';
                $output .= '<td>' . esc_html($giorno_nome) . ' (' . esc_html($data_str) . ')</td>';
                $output .= '<td>' . esc_html($ora_str) . '</td>';
                $output .= '<td>' . $stato . '</td>';
                if (!$is_prenotato) {
                    $output .= '<td><button class="sbc-book-btn" data-data="' . esc_attr($data_str) . '" data-ora="' . esc_attr($ora_str) . '">Prenota</button></td>';
                } else {
                    $output .= '<td>-</td>';
                }
                $output .= '</tr>';
                wp_reset_postdata();
            }
        }
    }
    $output .= '</tbody></table>';

    // Popup e form
    $output .= '<div id="sbc-booking-modal" style="display:none;position:fixed;top:0;left:0;width:100vw;height:100vh;background:rgba(0,0,0,0.5);z-index:9999;align-items:center;justify-content:center;">
        <div style="background:#fff;padding:20px;max-width:350px;margin:auto;position:relative;">
            <span id="sbc-close-modal" style="position:absolute;top:5px;right:10px;cursor:pointer;font-size:20px;">&times;</span>
            <h3>Prenota slot</h3>
            <form id="sbc-booking-form">
                <input type="hidden" name="data" id="sbc-form-data">
                <input type="hidden" name="ora" id="sbc-form-ora">
                <label for="sbc-form-nome">Nome:</label><br>
                <input type="text" name="nome" id="sbc-form-nome" required><br>
                <label for="sbc-form-telefono">Telefono:</label><br>
                <input type="text" name="telefono" id="sbc-form-telefono" required><br><br>
                <button type="submit">Conferma Prenotazione</button>
            </form>
            <div id="sbc-booking-success" style="display:none;color:green;margin-top:10px;"></div>
        </div>
    </div>';

    // JS inline
    $output .= '<script>
    document.addEventListener("DOMContentLoaded", function() {
        var modal = document.getElementById("sbc-booking-modal");
        var closeBtn = document.getElementById("sbc-close-modal");
        var form = document.getElementById("sbc-booking-form");
        var successMsg = document.getElementById("sbc-booking-success");
        document.querySelectorAll(".sbc-book-btn").forEach(function(btn) {
            btn.addEventListener("click", function() {
                document.getElementById("sbc-form-data").value = btn.getAttribute("data-data");
                document.getElementById("sbc-form-ora").value = btn.getAttribute("data-ora");
                form.style.display = "block";
                successMsg.style.display = "none";
                modal.style.display = "flex";
            });
        });
        closeBtn.onclick = function() { modal.style.display = "none"; };
        window.onclick = function(event) { if(event.target == modal) modal.style.display = "none"; };
        form.onsubmit = function(e) {
            e.preventDefault();
            var formData = new FormData(form);
            fetch("' . admin_url('admin-ajax.php') . '", {
                method: "POST",
                credentials: "same-origin",
                body: new URLSearchParams({
                    action: "sbc_book_slot",
                    data: formData.get("data"),
                    ora: formData.get("ora"),
                    nome: formData.get("nome"),
                    telefono: formData.get("telefono")
                })
            })
            .then(response => response.json())
            .then(data => {
                if(data.success) {
                    form.style.display = "none";
                    successMsg.innerText = data.data.message;
                    successMsg.style.display = "block";
                    setTimeout(function(){ location.reload(); }, 1500);
                } else {
                    successMsg.innerText = data.data.message || "Errore nella prenotazione.";
                    successMsg.style.display = "block";
                }
            });
        };
    });
    </script>';

    return $output;
}
add_shortcode('booking_calendar', 'sbc_render_booking_calendar');

// Gestione AJAX per prenotazione
add_action('wp_ajax_sbc_book_slot', 'sbc_book_slot_callback');
add_action('wp_ajax_nopriv_sbc_book_slot', 'sbc_book_slot_callback');
function sbc_book_slot_callback() {
    $data = sanitize_text_field($_POST['data']);
    $ora = sanitize_text_field($_POST['ora']);
    $nome = sanitize_text_field($_POST['nome']);
    $telefono = sanitize_text_field($_POST['telefono']);
    // Controlla se già prenotato
    $args = array(
        'post_type' => 'calendario',
        'meta_query' => array(
            array('key' => '_sbc_data', 'value' => $data, 'compare' => '='),
            array('key' => '_sbc_ora', 'value' => $ora, 'compare' => '='),
            array('key' => '_sbc_stato', 'value' => 'prenotato', 'compare' => '=')
        ),
        'posts_per_page' => 1
    );
    $prenotato = new WP_Query($args);
    if ($prenotato->have_posts()) {
        wp_send_json_error(array('message' => 'Slot già prenotato!'));
    }
    // Crea nuovo post calendario
    $post_id = wp_insert_post(array(
        'post_type' => 'calendario',
        'post_title' => 'Prenotazione ' . $data . ' ' . $ora,
        'post_status' => 'publish',
    ));
    if ($post_id) {
        update_post_meta($post_id, '_sbc_data', $data);
        update_post_meta($post_id, '_sbc_ora', $ora);
        update_post_meta($post_id, '_sbc_stato', 'prenotato');
        update_post_meta($post_id, '_sbc_nome', $nome);
        update_post_meta($post_id, '_sbc_telefono', $telefono);
        wp_send_json_success(array('message' => 'Prenotazione effettuata con successo!'));
    } else {
        wp_send_json_error(array('message' => 'Errore nella creazione della prenotazione.'));
    }
}
