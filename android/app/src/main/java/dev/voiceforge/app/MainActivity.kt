package dev.voiceforge.app

import android.annotation.SuppressLint
import android.app.Activity
import android.graphics.Color
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
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
 * Speak, Convert and Separate from the phone. The interface is the
 * same premium dark studio as the web GUI, styled to match.
 */
class MainActivity : Activity() {
    private lateinit var web: WebView
    private val prefs by lazy { getSharedPreferences("vf", MODE_PRIVATE) }

    private fun dp(n: Int): Int = (n * resources.displayMetrics.density).toInt()

    private fun rounded(fill: String, radius: Int, stroke: String? = null): GradientDrawable {
        return GradientDrawable().apply {
            setColor(Color.parseColor(fill))
            cornerRadius = dp(radius).toFloat()
            if (stroke != null) setStroke(dp(1), Color.parseColor(stroke))
        }
    }

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.statusBarColor = Color.parseColor("#0A0A0B")
        window.navigationBarColor = Color.parseColor("#0A0A0B")

        val bg = Color.parseColor("#0A0A0B")
        val panel = "#101012"
        val field = "#0D0D0F"
        val line = "#26262A"
        val dim = Color.parseColor("#A3A3AB")
        val dim2 = Color.parseColor("#6D6D75")

        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setBackgroundColor(bg)
        }

        val header = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setBackgroundColor(Color.parseColor(panel))
            setPadding(dp(18), dp(16), dp(18), dp(12))
        }
        header.addView(TextView(this).apply {
            text = "VoiceForge"
            setTextColor(Color.WHITE)
            textSize = 19f
            typeface = Typeface.DEFAULT_BOLD
        })
        header.addView(TextView(this).apply {
            text = "CPU Voice Cloning Studio"
            setTextColor(dim2)
            textSize = 12f
        })
        val bar = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            setPadding(0, dp(12), 0, 0)
        }
        val urlBox = EditText(this).apply {
            hint = "http://192.168.1.5:8760"
            setHintTextColor(dim2)
            setTextColor(Color.WHITE)
            textSize = 14f
            setSingleLine(true)
            background = rounded(field, 10, line)
            setPadding(dp(12), dp(10), dp(12), dp(10))
            setText(prefs.getString("url", ""))
            layoutParams = LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f)
        }
        val go = Button(this).apply {
            text = "Connect"
            isAllCaps = false
            setTextColor(Color.parseColor("#0A0A0B"))
            textSize = 14f
            typeface = Typeface.DEFAULT_BOLD
            background = rounded("#F5F5F4", 10)
            layoutParams = LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.WRAP_CONTENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            ).apply { marginStart = dp(10) }
        }
        bar.addView(urlBox)
        bar.addView(go)
        header.addView(bar)
        header.addView(TextView(this).apply {
            text = "Start VoiceForge on your computer with: voiceforge gui, then connect here on the same Wi-Fi."
            setTextColor(dim)
            textSize = 12f
            setPadding(0, dp(10), 0, 0)
        })
        root.addView(header)

        web = WebView(this).apply {
            setBackgroundColor(bg)
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
            val rest = if (url.startsWith("https://")) url.removePrefix("https://") else url.removePrefix("http://")
            if (!rest.contains(":")) url = "$url:8760"
            prefs.edit().putString("url", url).apply()
            web.loadUrl(url)
        }

        prefs.getString("url", null)?.let { saved ->
            urlBox.setText(saved)
            web.loadUrl(saved)
        }
        setContentView(root)
    }

    @Deprecated("Deprecated in Java")
    override fun onBackPressed() {
        if (web.canGoBack()) web.goBack() else super.onBackPressed()
    }
}
