import type {Stroke} from '../screens/CanvasScreen';

/**
 * Converts canvas strokes to a base64-encoded SVG image string.
 * In production this would use react-native-view-shot or similar,
 * but we serialize as SVG for transmission to the backend.
 */
export async function captureCanvasAsBase64(strokes: {path: string; color: string; width: number}[]): Promise<string> {
  const pathElements = strokes
    .map(
      s =>
        `<path d="${s.path}" stroke="${s.color}" stroke-width="${s.width}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`,
    )
    .join('\n');

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" style="background:white">\n${pathElements}\n</svg>`;

  // Encode to base64
  const encoded = encodeURIComponent(svg);
  return encoded;
}
