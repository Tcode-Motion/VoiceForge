package dev.voiceforge.app

import android.annotation.SuppressLint
import android.app.Activity
import android.os.Bundle
import android.webkit.PermissionRequest
import android.webkit.WebChromeClient
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.TextView

/**
 * VoiceForge companion for Android.
 *
 * The heavy engines (RVC, Demucs, Kokoro) run on your computer.
 * This app is the studio interface in your pocket: point it at
 * VoiceForge running on your PC (same Wi-Fi) and use Train, Sing,
 * Speak, Convert and Separate from the phone. 8 GB RAM phones run
 * this shell comfortably; the computer does the heavy lifting.
 */
class MainActivity : Activity() {
    private lateinit var web: WebView
    private val prefs by lazy { getSharedPreferences("vf", MODE_PRIVATE) }

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val root = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL }

        val bar = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL }
        val urlBox = EditText(this).apply {
            hint = "VoiceForge address, e.g. http://192.168.1.5:8760"
            setText(prefs.getString("url", ""))
            layoutParams = LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f)
        }
        val go = Button(this).apply { text = "Connect" }
        bar.addView(urlBox)
        bar.addView(go)
        root.addView(bar)

        val help = TextView(this).apply {
            text = "Start VoiceForge on your computer with: voiceforge gui -- then connect here."
            setPadding(16, 8, 16, 8)
        }
        root.addView(help)

        web = WebView(this).apply {
            settings.javaScriptEnabled = true
            settings.domStorageEnabled = true
            settings.mediaPlaybackRequiresUserGesture = false
            webViewClient = WebViewClient()
            webChromeClient = object : WebChromeClient() {
                override fun onPermissionRequest(request: PermissionRequest) {
                    request.grant(request.resources)
                }
            }
        }
        root.addView(web, LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.MATCH_PARENT, 0, 1f))

        go.setOnClickListener {
            var url = urlBox.text.toString().trim()
            if (url.isEmpty()) return@setOnClickListener
            if (!url.startsWith("http")) url = "http://$url"
            if (!url.contains(":", startIndex = 7)) url = "$url:8760"
            prefs.edit().putString("url", url).apply()
            web.loadUrl(url)
        }

        prefs.getString("url", null)?.let { saved ->
            urlBox.setText(saved)
            web.loadUrl(saved)
        }
        setContentView(root)
    }

    override fun onBackPressed() {
        if (web.canGoBack()) web.goBack() else super.onBackPressed()
    }
}
