import { useState, useEffect } from 'react'
import { View, Text, Input, Button } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { DEFAULT_SERVER } from '../../constants'
import './index.css'

export default function Settings() {
  const [server,  setServer]  = useState('')
  const [droneId, setDroneId] = useState('')
  const [posX,    setPosX]    = useState('')
  const [posY,    setPosY]    = useState('')

  useEffect(() => {
    setServer( Taro.getStorageSync('server')  || DEFAULT_SERVER)
    setDroneId(Taro.getStorageSync('droneId') || 'drone_A')
    setPosX(   Taro.getStorageSync('posX')    || '116')
    setPosY(   Taro.getStorageSync('posY')    || '39')
  }, [])

  const save = () => {
    Taro.setStorageSync('server',  server.trim())
    Taro.setStorageSync('droneId', droneId.trim())
    Taro.setStorageSync('posX',    posX.trim())
    Taro.setStorageSync('posY',    posY.trim())
    Taro.showToast({ title: '已保存', icon: 'success' })
  }

  return (
    <View className='settings-page'>

      <View className='group'>
        <Text className='group-title'>服务器</Text>
        <View className='field'>
          <Text className='field-label'>地址</Text>
          <Input className='field-input' value={server} onInput={e => setServer(e.detail.value)} placeholder='http://127.0.0.1:5001' />
        </View>
      </View>

      <View className='group'>
        <Text className='group-title'>无人机</Text>
        <View className='field'>
          <Text className='field-label'>ID</Text>
          <Input className='field-input' value={droneId} onInput={e => setDroneId(e.detail.value)} placeholder='drone_A' />
        </View>
        <View className='field'>
          <Text className='field-label'>经度 X</Text>
          <Input className='field-input' type='number' value={posX} onInput={e => setPosX(e.detail.value)} placeholder='116' />
        </View>
        <View className='field'>
          <Text className='field-label'>纬度 Y</Text>
          <Input className='field-input' type='number' value={posY} onInput={e => setPosY(e.detail.value)} placeholder='39' />
        </View>
      </View>

      <Button className='save-btn' type='primary' onClick={save}>保存</Button>

    </View>
  )
}