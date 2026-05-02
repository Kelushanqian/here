import { useState, useEffect, useRef } from 'react'
import { View, Text, Image, ScrollView } from '@tarojs/components'
import { get, getServer } from '../../utils/request'
import { STATUS_LABEL, STATUS_COLOR, POLL_INTERVAL } from '../../constants'
import Taro from '@tarojs/taro'
import './index.css'

const FILTERS = ['全部', 'pending', 'processing', 'done', 'failed']

export default function Tasks() {
  const [images, setImages]     = useState([])
  const [filter, setFilter]     = useState('全部')
  const [preview, setPreview]   = useState(null)  // 当前全屏预览的图
  const timerRef = useRef(null)

  const load = () => get('/api/images').then(setImages).catch(console.error)

  useEffect(() => {
    load()
    timerRef.current = setInterval(load, POLL_INTERVAL)
    return () => clearInterval(timerRef.current)
  }, [])

  // 原来的 useEffect 保持不变（首次加载 + 轮询）
  useEffect(() => {
    load()
    timerRef.current = setInterval(load, POLL_INTERVAL)

    // 订阅上传完成事件
    Taro.eventCenter.on('images:updated', load)

    return () => {
      clearInterval(timerRef.current)
      Taro.eventCenter.off('images:updated', load)  // 卸载时记得取消订阅
    }
  }, [])

  const displayed = filter === '全部' ? images : images.filter(i => i.status === filter)
  const SERVER = getServer()

  return (
    <View className='tasks-page'>

      {/* 筛选条 */}
      <ScrollView scrollX className='filter-bar'>
        {FILTERS.map(f => (
          <Text
            key={f}
            className={`filter-chip ${filter === f ? 'active' : ''}`}
            onClick={() => setFilter(f)}
          >
            {f === '全部' ? '全部' : STATUS_LABEL[f]}
          </Text>
        ))}
      </ScrollView>

      {/* 列表 */}
      <ScrollView
        scrollY
        className='list'
        refresherEnabled
        onRefresherRefresh={() => load()}
      >
        {displayed.length === 0 ? (
          <View className='empty'>暂无数据</View>
        ) : (
          displayed.map(item => (
            <View key={item.id} className='card'>

              {/* 头部：无人机信息 + 状态 */}
              <View className='card-header'>
                <View>
                  <Text className='drone-tag'>{item.drone_id}</Text>
                  <Text className='coord'>({item.x}, {item.y})</Text>
                </View>
                <View className='status-pill' style={`background:${STATUS_COLOR[item.status]}1a;color:${STATUS_COLOR[item.status]}`}>
                  <Text>{STATUS_LABEL[item.status] ?? item.status}</Text>
                </View>
              </View>

              <Text className='time'>{item.capture_time}</Text>

              {/* 双图对比 */}
              <View className='img-row'>
                <View className='img-wrap' onClick={() => setPreview(`${SERVER}/images/original/${item.original_filename}`)}>
                  <Image src={`${SERVER}/images/original/${item.original_filename}`} mode='aspectFill' className='thumb' />
                  <Text className='img-label'>原图</Text>
                </View>
                <View className='divider' />
                <View className='img-wrap'>
                  {item.status === 'done' ? (
                    <>
                      <Image
                        src={`${SERVER}/images/processed/${item.processed_filename}`}
                        mode='aspectFill'
                        className='thumb'
                        onClick={() => setPreview(`${SERVER}/images/processed/${item.processed_filename}`)}
                      />
                      <Text className='img-label'>处理后</Text>
                    </>
                  ) : (
                    <View className='pending-box' style={`border-color:${STATUS_COLOR[item.status]}`}>
                      <Text className='pending-text' style={`color:${STATUS_COLOR[item.status]}`}>
                        {STATUS_LABEL[item.status]}
                      </Text>
                    </View>
                  )}
                </View>
              </View>

            </View>
          ))
        )}
      </ScrollView>

      {/* 全屏预览浮层 */}
      {preview && (
        <View className='preview-mask' onClick={() => setPreview(null)}>
          <Image src={preview} mode='aspectFit' className='preview-img' />
          <Text className='preview-close'>点击关闭</Text>
        </View>
      )}

    </View>
  )
}