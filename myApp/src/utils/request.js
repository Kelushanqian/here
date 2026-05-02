import Taro from '@tarojs/taro'
import { DEFAULT_SERVER } from '../constants'

export function getServer() {
  return Taro.getStorageSync('server') || DEFAULT_SERVER
}

export async function get(path) {
  const res = await Taro.request({
    url: `${getServer()}${path}`,
    method: 'GET',
  })
  if (res.statusCode !== 200) throw new Error(`HTTP ${res.statusCode}`)
  return res.data
}