import { useState } from 'react'
import { View, Text, Image, Button, ScrollView, Video } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { getServer } from '../../utils/request'
import './index.css'

export default function Upload() {
  const [files, setFiles]         = useState([])   // { tempFilePath, name, fileType }[]
  const [uploading, setUploading] = useState(false)

  const droneId = Taro.getStorageSync('droneId') || 'drone_A'
  const x       = Taro.getStorageSync('posX')    || 116
  const y       = Taro.getStorageSync('posY')    || 39

  const pick = async () => {
    try {
      const res = await Taro.chooseMedia({
        count: 9,
        mediaType: ['image', 'video'],   // 加上 video
        sourceType: ['album', 'camera']
      })
      setFiles(prev => [
        ...prev,
        ...res.tempFiles.map(f => ({
          tempFilePath: f.tempFilePath,
          name: f.tempFilePath.split('/').pop(),
          fileType: f.fileType   // 'image' 或 'video'
        }))
      ])
    } catch (e) { /* 用户取消 */ }
  }

  const remove = (idx) => setFiles(prev => prev.filter((_, i) => i !== idx))

  const submit = async () => {
    if (!files.length) return
    setUploading(true)
    const SERVER = getServer()

    const uploads = files.map(file => {
      const isVideo = file.fileType === 'video'
      return new Promise(resolve => {
        Taro.uploadFile({
          url: `${SERVER}${isVideo ? '/api/ingest_video' : '/api/ingest'}`,
          filePath: file.tempFilePath,
          name: 'file',
          formData: { drone_id: droneId, x, y, interval_seconds: 5 },
          success: resolve,
          fail: (err) => { console.error(err); resolve() },
        })
      })
    })

    await Promise.all(uploads)
    setUploading(false)
    setFiles([])
    Taro.showToast({ title: `${uploads.length} 个文件已提交`, icon: 'success' })
    Taro.eventCenter.trigger('images:updated')
  }

  return (
    <ScrollView scrollY className='upload-page'>

      <View className='upload-zone' onClick={pick}>
        <Text className='upload-icon'>＋</Text>
        <Text className='upload-hint'>点击选择图片或视频（最多 9 个）</Text>
      </View>

      <View className='param-bar'>
        <Text className='param-item'>无人机：{droneId}</Text>
        <Text className='param-item'>坐标：({x}, {y})</Text>
      </View>

      {files.length > 0 && (
        <>
          <View className='preview-grid'>
            {files.map((f, idx) => (
              <View key={idx} className='preview-item'>
                {f.fileType === 'video'
                  ? <Video
                      src={f.tempFilePath}
                      className='preview-thumb'
                      controls={false}
                      autoplay={false}
                    />
                  : <Image src={f.tempFilePath} mode='aspectFill' className='preview-thumb' />
                }
                <View className='remove-btn' onClick={() => remove(idx)}>
                  <Text className='remove-x'>×</Text>
                </View>
              </View>
            ))}
          </View>

          <View className='submit-area'>
            <Button
              className='submit-btn'
              type='primary'
              loading={uploading}
              disabled={uploading}
              onClick={submit}
            >
              {uploading ? '上传中…' : `提交 ${files.length} 个`}
            </Button>
            <Button className='clear-btn' onClick={() => setFiles([])}>清空</Button>
          </View>
        </>
      )}

    </ScrollView>
  )
}