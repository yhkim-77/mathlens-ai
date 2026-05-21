import type {Stroke} from '../screens/CanvasScreen';

/**
 * Converts canvas strokes to a base64-encoded SVG image string.
 * Serializes the drawn strokes as an SVG document and encodes it as
 * a base64 data URL suitable for transmission to the backend analyze API.
 */
export async function captureCanvasAsBase64(strokes: {path: string; color: string; width: number}[]): Promise<string> {
  const pathElements = strokes
    .map(
      s =>
        `<path d="${s.path}" stroke="${s.color}" stroke-width="${s.width}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`,
    )
    .join('\n');

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" style="background:white">\n${pathElements}\n</svg>`;

  // Encode SVG to base64 using Buffer (available in React Native's Hermes)
  const encoded = Buffer.from(svg, 'utf8').toString('base64');
  return encoded;
}
