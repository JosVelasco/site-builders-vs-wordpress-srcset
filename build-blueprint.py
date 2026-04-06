#!/usr/bin/env python3
"""
Build blueprint.json for the Dorian Gray Code Workshop.
Run after any change to mu-plugin.php to keep the inline copy current.
"""
import json

with open('mu-plugin.php', 'r') as f:
    mu_plugin_content = f.read()

# ── Checklist + pages PHP ─────────────────────────────────────────────────────
setup_php = r"""<?php
require_once '/wordpress/wp-load.php';

$upload_dir = wp_upload_dir();
$hero_file  = $upload_dir['basedir'] . '/hero-landscape.jpg';
$filetype   = wp_check_filetype( basename( $hero_file ), null );

$attachment = array(
    'guid'           => $upload_dir['baseurl'] . '/hero-landscape.jpg',
    'post_mime_type' => $filetype['type'],
    'post_title'     => 'Hero Landscape',
    'post_content'   => '',
    'post_status'    => 'inherit',
);
$hero_id = wp_insert_attachment( $attachment, $hero_file );

require_once ABSPATH . 'wp-admin/includes/image.php';
$attach_data = wp_generate_attachment_metadata( $hero_id, $hero_file );
wp_update_attachment_metadata( $hero_id, $attach_data );
$hero_url = wp_get_attachment_url( $hero_id );

// --- Elementor page ---
$el_data = json_encode( array(
    array(
        'id'       => 'a1b2c3d4',
        'elType'   => 'section',
        'isInner'  => false,
        'settings' => array(
            'background_background' => 'classic',
            'background_image'      => array(
                'url'    => $hero_url,
                'id'     => $hero_id,
                'alt'    => '',
                'source' => 'library',
            ),
            'background_size'               => 'cover',
            'background_position'           => 'center center',
            'background_overlay_background' => 'classic',
            'background_overlay_color'      => 'rgba(0,0,0,0.45)',
            'height'                        => 'min-height',
            'custom_height'       => array( 'unit' => 'vh', 'size' => 70, 'sizes' => array() ),
            'content_position'    => 'middle',
        ),
        'elements' => array(
            array(
                'id'       => 'e1f2g3h4',
                'elType'   => 'column',
                'isInner'  => false,
                'settings' => array( '_column_size' => 100, 'content_position' => 'middle' ),
                'elements' => array(
                    array(
                        'id'         => 'i1j2k3l4',
                        'elType'     => 'widget',
                        'isInner'    => false,
                        'widgetType' => 'heading',
                        'settings'   => array(
                            'title'                 => 'Beautiful. Responsive. Or Is It?',
                            'title_color'           => '#ffffff',
                            'typography_typography' => 'custom',
                            'typography_font_size'  => array( 'unit' => 'px', 'size' => 48, 'sizes' => array() ),
                            'align'                 => 'center',
                        ),
                    ),
                    array(
                        'id'         => 'm1n2o3p4',
                        'elType'     => 'widget',
                        'isInner'    => false,
                        'widgetType' => 'text-editor',
                        'settings'   => array(
                            'editor' => '<p style="color: #ffffff; font-size: 20px; text-align: center;">This hero image looks perfect. Open DevTools Network tab to see what the browser actually downloaded.</p>',
                        ),
                    ),
                    array(
                        'id'         => 'q1r2s3t4',
                        'elType'     => 'widget',
                        'isInner'    => false,
                        'widgetType' => 'text-editor',
                        'settings'   => array(
                            'editor' => '<p style="color: #cccccc; font-size: 12px; text-align: center;">Photo: <a href="https://wordpress.org/photos/photo/206524fb22/" style="color:#cccccc;">Sagar Tamang</a> &middot; WordPress Photo Directory &middot; CC0</p>',
                        ),
                    ),
                ),
            ),
        ),
    ),
), JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE );

$elementor_page_id = wp_insert_post( array(
    'post_title'     => 'Elementor Page',
    'post_name'      => 'elementor-page',
    'post_status'    => 'publish',
    'post_type'      => 'page',
    'comment_status' => 'closed',
) );
update_post_meta( $elementor_page_id, '_elementor_edit_mode',     'builder' );
update_post_meta( $elementor_page_id, '_elementor_template_type', 'wp-page' );
update_post_meta( $elementor_page_id, '_elementor_version',       '3.35.5' );
update_post_meta( $elementor_page_id, '_wp_page_template',        'elementor_canvas' );
update_post_meta( $elementor_page_id, '_elementor_data', wp_slash( $el_data ) );

// --- Native editor page ---
$srcset = wp_get_attachment_image_srcset( $hero_id, 'full' );
$sizes  = wp_get_attachment_image_sizes( $hero_id, 'full' );
$img    = '<img class="wp-block-cover__image-background wp-image-' . $hero_id . '" alt="" src="' . $hero_url . '" data-object-fit="cover"';
if ( $srcset ) { $img .= ' srcset="' . esc_attr( $srcset ) . '"'; }
if ( $sizes )  { $img .= ' sizes="'  . esc_attr( $sizes )  . '"'; }
$img .= '/>';

$cover  = '<!-- wp:cover {"url":"' . $hero_url . '","id":' . $hero_id . ',"dimRatio":40,"minHeight":70,"minHeightUnit":"vh","isDark":false,"align":"full"} -->' . "\n";
$cover .= '<div class="wp-block-cover alignfull" style="min-height:70vh">' . "\n";
$cover .= '<span aria-hidden="true" class="wp-block-cover__background has-background-dim-40 has-background-dim"></span>' . "\n";
$cover .= $img . "\n";
$cover .= '<div class="wp-block-cover__inner-container">' . "\n";
$cover .= '<!-- wp:heading {"textAlign":"center","style":{"color":{"text":"#ffffff"}}} -->' . "\n";
$cover .= '<h2 class="wp-element-heading has-text-align-center has-text-color" style="color:#ffffff">Beautiful. Responsive. And Actually Responsive.</h2>' . "\n";
$cover .= '<!-- /wp:heading -->' . "\n";
$cover .= '<!-- wp:paragraph {"align":"center","style":{"color":{"text":"#ffffff"}}} -->' . "\n";
$cover .= '<p class="has-text-align-center has-text-color" style="color:#ffffff">This hero image looks identical. View page source and search for srcset. Then compare with the Elementor page.</p>' . "\n";
$cover .= '<!-- /wp:paragraph -->' . "\n";
$cover .= '</div></div>' . "\n";
$cover .= '<!-- /wp:cover -->' . "\n";
$cover .= '<!-- wp:paragraph -->' . "\n";
$cover .= '<p style="text-align:center;color:#888888;font-size:12px;">Photo: <a href="https://wordpress.org/photos/photo/206524fb22/" style="color:#888888;">Sagar Tamang</a> &middot; WordPress Photo Directory &middot; CC0</p>' . "\n";
$cover .= '<!-- /wp:paragraph -->';

$native_page_id = wp_insert_post( array(
    'post_title'     => 'Native Editor',
    'post_name'      => 'native-editor',
    'post_status'    => 'publish',
    'post_type'      => 'page',
    'post_content'   => $cover,
    'comment_status' => 'closed',
) );

// --- Checklist page ---
$checklist_pid = wp_insert_post( array(
    'post_title'     => 'Workshop Checklist',
    'post_name'      => 'workshop-checklist',
    'post_status'    => 'publish',
    'post_type'      => 'page',
    'post_content'   => '',
    'comment_status' => 'closed',
) );

$ep_url = home_url( '/elementor-page/' );
$ne_url = home_url( '/native-editor/' );

$c  = '<!-- wp:paragraph --><p>Two pages. Same hero image. One built with Elementor, one with the native editor. Your job: find out whether the browser can serve the right image size to the right screen — or whether every visitor gets the same file regardless of their device.</p><!-- /wp:paragraph -->';

$c .= '<!-- wp:heading --><h2 class="wp-block-heading">Task 1: Find srcset on the Native Editor Page</h2><!-- /wp:heading -->';
$c .= '<!-- wp:paragraph --><p>Go to <a href="' . $ne_url . '"><strong>/native-editor/</strong></a>. Right-click the hero image and choose <strong>Inspect</strong>. In the Elements tab, hover over the <code>&lt;img&gt;</code> tag — you will see the full element including the <code>srcset</code> attribute. Right-click the tag and choose <strong>Copy &rarr; Copy element</strong> and paste it in your notes.</p><!-- /wp:paragraph -->';
$c .= '<!-- wp:paragraph --><p><strong>Discussion:</strong> How many size variants are listed? What does the number after each URL (e.g. <code>768w</code>) mean?</p><!-- /wp:paragraph -->';

$c .= '<!-- wp:heading --><h2 class="wp-block-heading">Task 2: Look for srcset on the Elementor Page</h2><!-- /wp:heading -->';
$c .= '<!-- wp:paragraph --><p>Go to <a href="' . $ep_url . '"><strong>/elementor-page/</strong></a>. Right-click the hero area and choose <strong>Inspect</strong>. Look at the element that carries the background image — what tag is it? Does it have a <code>srcset</code> attribute? Copy the element to your notes.</p><!-- /wp:paragraph -->';
$c .= '<!-- wp:paragraph --><p><strong>Discussion:</strong> Why is there no srcset? What does using a CSS background instead of an img tag cost the visitor?</p><!-- /wp:paragraph -->';

$c .= '<!-- wp:heading --><h2 class="wp-block-heading">Task 3: See Which Image the Browser Actually Downloaded</h2><!-- /wp:heading -->';
$c .= '<!-- wp:paragraph --><p>Open DevTools (Mac: Cmd+Option+I, Windows: Ctrl+Shift+I) and go to the Network tab. Check <strong>Disable cache</strong>, then filter by <strong>Img</strong>. Reload <a href="' . $ep_url . '"><strong>/elementor-page/</strong></a> and note the image filename. Do the same on <a href="' . $ne_url . '"><strong>/native-editor/</strong></a>.</p><!-- /wp:paragraph -->';
$c .= '<!-- wp:paragraph --><p><strong>Note:</strong> The Size column will show <em>(ServiceWorker)</em> — that is normal for Playground. Focus on the filename. Also, do not hard-reload (Cmd+Shift+R / Ctrl+Shift+F5) — it breaks Playground.</p><!-- /wp:paragraph -->';
$c .= '<!-- wp:paragraph --><p><strong>Discussion:</strong> Are the filenames the same? Does one include dimensions in the name (e.g. <code>-1024x473</code>)?</p><!-- /wp:paragraph -->';

$c .= '<!-- wp:heading --><h2 class="wp-block-heading">Task 4: Shrink the Viewport and Reload</h2><!-- /wp:heading -->';
$c .= '<!-- wp:paragraph --><p>Drag your browser window to roughly 400 px wide. With <strong>Disable cache</strong> still checked, reload <a href="' . $ne_url . '"><strong>/native-editor/</strong></a>. What is the filename now? Compare it with what you saw in Task 3. Do the same on <a href="' . $ep_url . '"><strong>/elementor-page/</strong></a> — does the filename change?</p><!-- /wp:paragraph -->';
$c .= '<!-- wp:paragraph --><p><strong>Discussion:</strong> What does the filename difference tell you about what a mobile visitor actually downloads?</p><!-- /wp:paragraph -->';

$c .= '<!-- wp:heading --><h2 class="wp-block-heading">Task 5: Read the srcset and sizes Attributes</h2><!-- /wp:heading -->';
$c .= '<!-- wp:paragraph --><p>On <a href="' . $ne_url . '"><strong>/native-editor/</strong></a>, open the DevTools Elements tab and click the img element inside the hero. Find the <code>srcset</code> and <code>sizes</code> attributes in the markup. How many candidate URLs are listed? What does the <code>sizes</code> value instruct the browser to do?</p><!-- /wp:paragraph -->';
$c .= '<!-- wp:paragraph --><p><strong>Discussion:</strong> Who wrote those attributes — you, or WordPress?</p><!-- /wp:paragraph -->';

$c .= '<!-- wp:heading --><h2 class="wp-block-heading">Discussion</h2><!-- /wp:heading -->';
$c .= '<!-- wp:paragraph --><p>Think about what you found. We will discuss as a group at the end.</p><!-- /wp:paragraph -->';

wp_update_post( array( 'ID' => $checklist_pid, 'post_content' => $c ) );
"""

# ── Quiz PHP ──────────────────────────────────────────────────────────────────
quiz_php = r"""<?php
require_once '/wordpress/wp-load.php';

global $wpdb;

$wpdb->insert( $wpdb->prefix . 'mlw_quizzes', array(
    'quiz_name'          => 'Site Builders vs WordPress: srcset – Knowledge Check',
    'randomness_order'   => 2,
    'show_score'         => 1,
    'total_user_tries'   => 0,
    'ajax_show_correct'  => 1,
    'require_log_in'     => 0,
    'user_name'          => 2,
    'user_comp'          => 2,
    'user_email'         => 2,
    'user_phone'         => 2,
    'comment_section'    => 1,
    'deleted'            => 0,
    'quiz_views'         => 0,
    'quiz_taken'         => 0,
    'last_activity'      => current_time( 'mysql' ),
    'submit_button_text' => 'Submit Answers',
    'message_before'     => '',
    'message_after'      => '',
) );
$quiz_id = $wpdb->insert_id;

function dg_q( $quiz_id, $text, $answers, $correct_idx ) {
    global $wpdb;
    $arr = array();
    foreach ( $answers as $i => $a ) {
        $arr[] = array( $a, ( $i === $correct_idx ) ? 1 : 0, ( $i === $correct_idx ) ? 1 : 0, '' );
    }
    $wpdb->insert( $wpdb->prefix . 'mlw_questions', array(
        'quiz_id'               => $quiz_id,
        'question_name'         => $text,
        'answer_array'          => maybe_serialize( $arr ),
        'correct_answer'        => $correct_idx + 1,
        'question_type'         => 0,
        'question_type_new'     => '0',
        'question_order'        => 0,
        'comments'              => 1,
        'question_settings'     => maybe_serialize( array( 'Required' => '0' ) ),
        'deleted'               => 0,
        'deleted_question_bank' => 0,
    ) );
    return $wpdb->insert_id;
}

$qids = array();

$qids[] = dg_q( $quiz_id,
    'What does the srcset attribute on an img tag do?',
    array(
        'Adds a decorative border around the image',
        'Provides multiple image size candidates so the browser can download the most appropriate one for the current viewport',
        'Compresses the image before it reaches the browser',
        'Prevents the image from being indexed by search engines',
    ),
    1
);

$qids[] = dg_q( $quiz_id,
    'Why does the Elementor hero section have no srcset?',
    array(
        'Elementor compresses images separately so srcset is unnecessary',
        'Elementor uses a CSS background-image for the hero, and CSS backgrounds cannot carry a srcset attribute',
        'WordPress removes srcset from images used inside page builders',
        'srcset only works on images smaller than 300 px',
    ),
    1
);

$qids[] = dg_q( $quiz_id,
    'What does the sizes attribute in an img tag tell the browser?',
    array(
        'The physical dimensions of the image file in pixels',
        'How many colour channels the image contains',
        'How wide the image will be rendered at different viewport sizes, so the browser can pick the right srcset candidate',
        'The maximum file size the browser should download',
    ),
    2
);

$qids[] = dg_q( $quiz_id,
    'If a page has no srcset on its hero image, what does a visitor on a 390 px phone screen download?',
    array(
        'A thumbnail automatically created by the browser',
        'The same full-resolution image as a visitor on a 2560 px desktop monitor',
        'A placeholder until the page fully loads',
        'Nothing -- the browser skips images it cannot resize',
    ),
    1
);

$qids[] = dg_q( $quiz_id,
    'How does WordPress generate the multiple image sizes listed in a srcset?',
    array(
        'It calls an external image CDN at display time',
        'It creates resized copies when the image is uploaded to the Media Library',
        'It resizes images on the fly for each visitor',
        'It relies on the active theme to define sizes at activation',
    ),
    1
);

$qids[] = dg_q( $quiz_id,
    'In DevTools, which tab lets you see the exact filename and byte size of the image the browser actually downloaded?',
    array(
        'Elements',
        'Console',
        'Network',
        'Sources',
    ),
    2
);

$qids[] = dg_q( $quiz_id,
    'On a narrow mobile viewport, the native editor page downloaded a smaller image than the Elementor page. What is the practical consequence for users?',
    array(
        'The native editor page loads a lower-quality image that looks blurry on mobile',
        'The Elementor page uses more mobile data and takes longer to load because it always serves the full-resolution file',
        'Both pages transfer the same amount of data -- only the display size changes',
        'The Elementor page caches the image locally to avoid re-downloading it',
    ),
    1
);

$qids[] = dg_q( $quiz_id,
    'Which WordPress function returns a complete img tag with srcset and sizes attributes already included?',
    array(
        'get_the_post_thumbnail_url() -- returns just the image URL as a string',
        'wp_get_attachment_image() -- returns a full img tag including srcset and sizes',
        'wp_get_attachment_url() -- returns just the file URL',
        'get_image_tag() -- returns an img tag without responsive attributes',
    ),
    1
);

$wpdb->update(
    $wpdb->prefix . 'mlw_quizzes',
    array( 'quiz_settings' => maybe_serialize( array(
        'pages'                  => array( $qids ),
        'enable_quick_result_mc' => 1,
    ) ) ),
    array( 'quiz_id' => $quiz_id )
);

$quiz_post_id = wp_insert_post( array(
    'post_title'   => 'Site Builders vs WordPress: srcset – Knowledge Check',
    'post_content' => '[mlw_quizmaster quiz=' . $quiz_id . ']',
    'post_status'  => 'publish',
    'post_author'  => get_current_user_id(),
    'post_type'    => 'qsm_quiz',
) );
add_post_meta( $quiz_post_id, 'quiz_id', intval( $quiz_id ) );

$kid = wp_insert_post( array(
    'post_title'   => 'Knowledge Check',
    'post_name'    => 'knowledge-check',
    'post_status'  => 'publish',
    'post_type'    => 'page',
    'post_content' => '',
) );
$shortcode = '[mlw_quizmaster quiz=' . $quiz_id . ']';
$k  = '<!-- wp:paragraph --><p>Eight questions based on what you just explored. Click an answer to see immediately whether you were right.</p><!-- /wp:paragraph -->';
$k .= '<!-- wp:shortcode -->' . $shortcode . '<!-- /wp:shortcode -->';
wp_update_post( array( 'ID' => $kid, 'post_content' => $k ) );

$checklist = get_page_by_path( 'workshop-checklist' );
if ( $checklist ) {
    $quiz_url = get_permalink( $kid );
    $q  = '<!-- wp:separator --><hr class="wp-block-separator has-alpha-channel-opacity"/><!-- /wp:separator -->';
    $q .= '<!-- wp:heading {"level":2} --><h2 class="wp-block-heading">Knowledge Check</h2><!-- /wp:heading -->';
    $q .= '<!-- wp:paragraph --><p>Finished all five tasks? Head to the <a href="' . $quiz_url . '">Knowledge Check</a> to confirm what you have learned.</p><!-- /wp:paragraph -->';
    wp_update_post( array( 'ID' => $checklist->ID, 'post_content' => $checklist->post_content . $q ) );
}

echo 'quiz done';
"""

# ── Blueprint ─────────────────────────────────────────────────────────────────
blueprint = {
    "$schema": "https://playground.wordpress.net/blueprint-schema.json",
    "landingPage": "/wp-admin",
    "login": True,
    "preferredVersions": {
        "php": "8.2",
        "wp": "6.9"
    },
    "steps": [
        # Suppress Elementor onboarding before install
        {
            "step": "wp-cli",
            "command": "wp option update elementor_onboarded 1 --allow-root"
        },
        {
            "step": "wp-cli",
            "command": "wp option update elementor_install_time 1 --allow-root"
        },
        {
            "step": "wp-cli",
            "command": "wp option update elementor_onboarding_opt_in yes --allow-root"
        },
        # Theme — twentytwentyfive ships with WP 6.9 and has native alignfull support
        {
            "step": "wp-cli",
            "command": "wp theme activate twentytwentyfive --allow-root"
        },
        # Plugins
        {
            "step": "wp-cli",
            "command": "wp user meta update 1 elementor_introduction '{\"e-editor-one-notice-pointer\":true}' --format=json --allow-root"
        },
        {
            "step": "installPlugin",
            "pluginData": {
                "resource": "wordpress.org/plugins",
                "slug": "elementor"
            }
        },
        {
            "step": "installPlugin",
            "pluginData": {
                "resource": "wordpress.org/plugins",
                "slug": "quiz-master-next"
            }
        },
        # Disable QSM new render mode
        {
            "step": "wp-cli",
            "command": "wp option update qmn-settings '{\"enable_new_render\":0}' --format=json --allow-root"
        },
        # Images
        {
            "step": "mkdir",
            "path": "/wordpress/wp-content/uploads"
        },
        {
            "step": "writeFile",
            "path": "/wordpress/wp-content/uploads/hero-landscape.jpg",
            "data": {
                "resource": "url",
                "url": "https://cdn.jsdelivr.net/gh/JosVelasco/site-builders-vs-wordpress-srcset@35ab0f5/hero-landscape.jpg"
            }
        },
        {
            "step": "writeFile",
            "path": "/wordpress/wp-content/uploads/dorian-wp-workshop.jpg",
            "data": {
                "resource": "url",
                "url": "https://cdn.jsdelivr.net/gh/JosVelasco/site-builders-vs-wordpress-srcset@35ab0f5/dorian-wp-workshop.jpg"
            }
        },
        # Create pages
        {
            "step": "runPHP",
            "code": setup_php
        },
        # mu-plugin (inlined)
        {
            "step": "mkdir",
            "path": "/wordpress/wp-content/mu-plugins"
        },
        {
            "step": "writeFile",
            "path": "/wordpress/wp-content/mu-plugins/dorian-workshop.php",
            "data": mu_plugin_content
        },
        # Quiz
        {
            "step": "runPHP",
            "code": quiz_php
        },
    ]
}

with open('blueprint.json', 'w') as f:
    json.dump(blueprint, f, indent=2, ensure_ascii=False)

print("blueprint.json written.")
print(f"mu-plugin.php inlined: {len(mu_plugin_content)} chars")
