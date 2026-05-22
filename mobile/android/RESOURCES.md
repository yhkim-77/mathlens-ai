# Android Resource Requirements

This document describes the required Android resources for the MathLens AI mobile application.

## Required Launcher Icons

The following launcher icons must be present for the Android build to succeed:

### Directory Structure
```
app/src/main/res/
├── mipmap-mdpi/
│   ├── ic_launcher.png (48x48)
│   └── ic_launcher_round.png (48x48)
├── mipmap-hdpi/
│   ├── ic_launcher.png (72x72)
│   └── ic_launcher_round.png (72x72)
├── mipmap-xhdpi/
│   ├── ic_launcher.png (96x96)
│   └── ic_launcher_round.png (96x96)
├── mipmap-xxhdpi/
│   ├── ic_launcher.png (144x144)
│   └── ic_launcher_round.png (144x144)
└── mipmap-xxxhdpi/
    ├── ic_launcher.png (192x192)
    └── ic_launcher_round.png (192x192)
```

### Icon Types

1. **ic_launcher.png** - Standard square launcher icon
2. **ic_launcher_round.png** - Round launcher icon for devices that support circular icons

### Densities

Android requires icons in multiple densities to support different screen resolutions:

- **mdpi** (Medium) - ~160dpi - 48×48 px
- **hdpi** (High) - ~240dpi - 72×72 px
- **xhdpi** (Extra High) - ~320dpi - 96×96 px
- **xxhdpi** (Extra Extra High) - ~480dpi - 144×144 px
- **xxxhdpi** (Extra Extra Extra High) - ~640dpi - 192×192 px

## Validation

Before building, you can validate that all required resources are present:

```bash
cd mobile/android
./validate-resources.sh
```

This script will:
- Check for all required launcher icon files
- Verify AndroidManifest.xml exists and references the icons correctly
- Check for required values resources (strings.xml, styles.xml)
- Warn about any missing drawable resources referenced in XML files

## CI/CD Integration

The validation script is automatically run in GitHub Actions CI/CD pipelines before building:
- **CI workflow** (`.github/workflows/ci.yml`) - Runs on pull requests and pushes to main
- **Release workflow** (`.github/workflows/release.yml`) - Runs on version tags

This ensures that build failures due to missing resources are caught early.

## Generating Icons

If you need to create new launcher icons, you can use:

1. **Android Studio's Image Asset Studio**
   - Right-click on `app/src/main/res` → New → Image Asset
   - Select "Launcher Icons (Adaptive and Legacy)"
   - Choose your source image and configure
   - Studio will generate all required densities

2. **Online Tools**
   - [Android Asset Studio](https://romannurik.github.io/AndroidAssetStudio/icons-launcher.html)
   - [Icon Kitchen](https://icon.kitchen/)

3. **Command Line (ImageMagick)**
   ```bash
   # From a 512x512 source image
   convert source.png -resize 48x48 mipmap-mdpi/ic_launcher.png
   convert source.png -resize 72x72 mipmap-hdpi/ic_launcher.png
   convert source.png -resize 96x96 mipmap-xhdpi/ic_launcher.png
   convert source.png -resize 144x144 mipmap-xxhdpi/ic_launcher.png
   convert source.png -resize 192x192 mipmap-xxxhdpi/ic_launcher.png
   ```

## Other Required Resources

### values/strings.xml
Must contain at least:
```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">MathLens AI</string>
</resources>
```

### values/styles.xml
Should define the application theme. Avoid referencing non-existent drawable resources.

## Troubleshooting

### Build Error: "resource mipmap/ic_launcher not found"
**Solution**: Run `./validate-resources.sh` to identify which icon files are missing, then generate them.

### Build Error: "resource drawable/xyz not found"
**Solution**: Either create the missing drawable resource or remove the reference from styles.xml/other XML files.

### Icons appear blurry on some devices
**Solution**: Ensure you have provided icons for all density buckets (mdpi through xxxhdpi). Android will scale the nearest density if a specific size is missing.

## References

- [Android App Icons Guide](https://developer.android.com/guide/practices/ui_guidelines/icon_design_launcher)
- [Supporting Multiple Screens](https://developer.android.com/guide/practices/screens_support)
- [Android Asset Studio](https://romannurik.github.io/AndroidAssetStudio/)
