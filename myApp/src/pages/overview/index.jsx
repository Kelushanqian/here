import { useState, useEffect, useRef } from 'react'
import { View, Text, ScrollView } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { get } from '../../utils/request'
import { STATUS_LABEL, STATUS_COLOR, POLL_INTERVAL } from '../../constants'
import './index.css'

function aggregate(images) {
  const statusCount = { pending: 0, processing: 0, done: 0, failed: 0 }
  const droneMap = {}

  for (const img of images) {
    statusCount[img.status] = (statusCount[img.status] ?? 0) + 1
    if (!droneMap[img.drone_id]) droneMap[img.drone_id] = { total: 0, done: 0 }
    droneMap[img.drone_id].total++
    if (img.status === 'done') droneMap[img.drone_id].done++
  }

  return { statusCount, drones: Object.entries(droneMap) }
}

export default function Overview() {
  const [images, setImages]   = useState([])
  const [loading, setLoading] = useState(true)
  const timerRef = useRef(null)

  const load = () => {
    get('/api/images')
      .then(setImages)
      .catch(console.error)
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    load()
    timerRef.current = setInterval(load, POLL_INTERVAL)
    Taro.eventCenter.on('images:updated', load)

    return () => {
      clearInterval(timerRef.current)
      Taro.eventCenter.off('images:updated', load)
    }
  }, [])

  const { statusCount, drones } = aggregate(images)
  const total = images.length

  return (
    <ScrollView scrollY className='page'>

      {/* 顶部大数字 */}
      <View className='hero'>
        <Text className='hero-num'>{total}</Text>
        <Text className='hero-label'>图像总数</Text>
      </View>

      {/* 状态卡片 */}
      <View className='section-title'>处理状态</View>
      <View className='stat-row'>
        {Object.entries(statusCount).map(([key, count]) => (
          <View key={key} className='stat-card' style={`border-top: 4px solid ${STATUS_COLOR[key]}`}>
            <Text className='stat-num' style={`color:${STATUS_COLOR[key]}`}>{count}</Text>
            <Text className='stat-label'>{STATUS_LABEL[key]}</Text>
          </View>
        ))}
      </View>

      {/* 无人机列表 */}
      <View className='section-title'>无人机概况</View>
      {drones.length === 0 && !loading && (
        <View className='empty'>暂无数据</View>
      )}
      {drones.map(([droneId, stat]) => {
        const pct = stat.total ? Math.round(stat.done / stat.total * 100) : 0
        return (
          <View key={droneId} className='drone-card'>
            <View className='drone-header'>
              <Text className='drone-id'>{droneId}</Text>
              <Text className='drone-pct'>{pct}%</Text>
            </View>
            <Text className='drone-sub'>{stat.done}/{stat.total} 已完成</Text>
            {/* 进度条 */}
            <View className='progress-track'>
              <View className='progress-fill' style={`width:${pct}%;background:#1677ff`} />
            </View>
          </View>
        )
      })}
    </ScrollView>
  )
}