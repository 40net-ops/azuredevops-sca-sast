import type { Unit } from '@/types/units'

// Storage Units (Binary - IEC Standard)
export const STORAGE_UNITS: Unit[] = [
  {
    key: 'bit',
    label: 'Bit (bit)',
    category: 'storage',
    bytesMultiplier: 1 / 8,
    description: 'Smallest unit of data',
  },
  {
    key: 'byte',
    label: 'Byte (B)',
    category: 'storage',
    bytesMultiplier: 1,
    description: '8 bits',
  },
  {
    key: 'kb',
    label: 'Kilobyte (KB)',
    category: 'storage',
    bytesMultiplier: 1000,
    description: '1,000 bytes (decimal)',
  },
  {
    key: 'kib',
    label: 'Kibibyte (KiB)',
    category: 'storage',
    bytesMultiplier: 1024,
    description: '1,024 bytes (binary)',
  },
  {
    key: 'mb',
    label: 'Megabyte (MB)',
    category: 'storage',
    bytesMultiplier: 1000 ** 2,
    description: '1,000,000 bytes (decimal)',
  },
  {
    key: 'mib',
    label: 'Mebibyte (MiB)',
    category: 'storage',
    bytesMultiplier: 1024 ** 2,
    description: '1,048,576 bytes (binary)',
  },
  {
    key: 'gb',
    label: 'Gigabyte (GB)',
    category: 'storage',
    bytesMultiplier: 1000 ** 3,
    description: '1,000,000,000 bytes (decimal)',
  },
  {
    key: 'gib',
    label: 'Gibibyte (GiB)',
    category: 'storage',
    bytesMultiplier: 1024 ** 3,
    description: '1,073,741,824 bytes (binary)',
  },
  {
    key: 'tb',
    label: 'Terabyte (TB)',
    category: 'storage',
    bytesMultiplier: 1000 ** 4,
    description: '1,000,000,000,000 bytes (decimal)',
  },
  {
    key: 'tib',
    label: 'Tebibyte (TiB)',
    category: 'storage',
    bytesMultiplier: 1024 ** 4,
    description: '1,099,511,627,776 bytes (binary)',
  },
]

// Data Transfer Units
export const TRANSFER_UNITS: Unit[] = [
  {
    key: 'bps',
    label: 'Bits per second (bps)',
    category: 'transfer',
    bitsPerSecondMultiplier: 1,
    description: 'Basic data transfer rate',
  },
  {
    key: 'kbps',
    label: 'Kilobits per second (Kbps)',
    category: 'transfer',
    bitsPerSecondMultiplier: 1000,
    description: '1,000 bits per second',
  },
  {
    key: 'mbps',
    label: 'Megabits per second (Mbps)',
    category: 'transfer',
    bitsPerSecondMultiplier: 1000 ** 2,
    description: '1,000,000 bits per second',
  },
  {
    key: 'gbps',
    label: 'Gigabits per second (Gbps)',
    category: 'transfer',
    bitsPerSecondMultiplier: 1000 ** 3,
    description: '1,000,000,000 bits per second',
  },
  {
    key: 'Bps',
    label: 'Bytes per second (B/s)',
    category: 'transfer',
    bitsPerSecondMultiplier: 8,
    description: '8 bits per second',
  },
  {
    key: 'KBps',
    label: 'Kilobytes per second (KB/s)',
    category: 'transfer',
    bitsPerSecondMultiplier: 8 * 1000,
    description: '8,000 bits per second',
  },
  {
    key: 'MBps',
    label: 'Megabytes per second (MB/s)',
    category: 'transfer',
    bitsPerSecondMultiplier: 8 * 1000 ** 2,
    description: '8,000,000 bits per second',
  },
  {
    key: 'GBps',
    label: 'Gigabytes per second (GB/s)',
    category: 'transfer',
    bitsPerSecondMultiplier: 8 * 1000 ** 3,
    description: '8,000,000,000 bits per second',
  },
]

export const ALL_UNITS: Unit[] = [...STORAGE_UNITS, ...TRANSFER_UNITS]
