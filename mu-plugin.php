<?php
/**
 * Plugin Name: Site Builders vs WordPress – srcset
 * Description: Must-use plugin for the srcset episode of the Site Builders vs WordPress workshop series
 */

// Load Google Fonts in admin head (for notice chrome)
add_action( 'admin_head', function () {
	echo '<link rel="preconnect" href="https://fonts.googleapis.com">';
	echo '<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600&display=swap" rel="stylesheet">';
} );

// Load fonts inside the block editor canvas
add_action( 'enqueue_block_editor_assets', function () {
	echo '<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600&display=swap" rel="stylesheet">';
	wp_add_inline_style( 'wp-block-library', '
		.editor-styles-wrapper p,
		.wp-block-post-content p {
			font-size: 18px !important;
			font-family: system-ui, -apple-system, sans-serif !important;
		}
		.editor-styles-wrapper h2 {
			font-family: "Cinzel", serif !important;
			font-weight: 600 !important;
		}
	' );
} );

// Admin notice with banner and checklist link
add_action( 'admin_notices', function () {
	$checklist = get_page_by_path( 'workshop-checklist' );
	$url       = $checklist ? get_edit_post_link( $checklist->ID ) : admin_url();
	$img       = content_url( 'uploads/dorian-wp-workshop.jpg' );
	?>
	<div style="background:#1a1a1a;border:4px solid #b8960c;margin:10px 0 20px;overflow:hidden;">
		<img src="<?php echo esc_url( $img ); ?>" alt="Site Builders vs WordPress" style="display:block;width:100%;height:auto;">
		<div style="padding:16px 24px;color:#e8dcc8;">
			<p style="font-family:system-ui,-apple-system,sans-serif;font-size:18px;font-weight:normal;margin:0 0 14px;line-height:1.7;color:#e8dcc8;">Your page builder produces a hero that looks perfect on every screen. But has it created an img tag? Without one, there is no srcset — and without srcset, every visitor downloads the same full-resolution file.</p>
			<a href="<?php echo esc_url( $url ); ?>" style="font-family:'Cinzel',serif;color:#d4a843;font-size:22px;font-weight:600;text-decoration:underline;">&rarr; Open Workshop Checklist</a>
			<p style="font-size:12px;color:#888;margin:12px 0 0;">Photo: <a href="https://wordpress.org/photos/photo/206524fb22/" style="color:#888;">Sagar Tamang</a> &middot; WordPress Photo Directory &middot; CC0</p>
		</div>
	</div>
	<?php
} );

// Force the Cover block to break out of the theme's content container.
add_action( 'wp_head', function () {
	echo '<style>
		.wp-block-cover.alignfull {
			width: 100vw;
			max-width: 100vw;
			margin-left: calc(50% - 50vw);
			margin-right: calc(50% - 50vw);
		}
	</style>';
} );

// Quiz styles loaded in footer to override QSM's own stylesheet.
add_action( 'wp_footer', function () {
	echo '<style>
		.qsm-quiz-container.qmn_quiz_container .mlw_qmn_question p { font-weight: bold !important; }
		.qsm-submit-btn { display: none !important; }
		.mlw_custom_start { display: none !important; }
		.mlw_previous { display: none !important; }
		.quiz_section.qsm-question-wrapper { margin-bottom: 30px; }
	</style>';
}, 99 );
