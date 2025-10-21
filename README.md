# Computer Unit Converter

A modern, intuitive web application for converting between computer storage and data transfer units. Built with Vue 3, TypeScript, and Vuetify 3.

## Features

### Phase 1: MVP (Current)
- **Storage Unit Conversions**: Support for common storage units including:
  - Binary units (IEC): Bit, Byte, KiB, MiB, GiB, TiB
  - Decimal units (SI): KB, MB, GB, TB
- **Data Transfer Rate Conversions**: Support for transfer units including:
  - Bits per second: bps, Kbps, Mbps, Gbps
  - Bytes per second: B/s, KB/s, MB/s, GB/s
- **Real-time Conversion**: Instant conversion as you type
- **Conversion Formula Display**: See the math behind each conversion
- **Unit Swap**: Quickly swap source and target units
- **Copy to Clipboard**: One-click copy of conversion results
- **Light/Dark Theme**: Toggle between themes with localStorage persistence
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Educational Info**: Built-in information about binary vs. decimal units

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) to make the TypeScript language service aware of `.vue` types.

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```
