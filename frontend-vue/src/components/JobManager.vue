<template>
  <div class="card">
    <h2>⚙️ Job Control</h2>

    <div class="button-group">
      <button @click="createTimelapse">⏱️ Timelapse</button>
      <button @click="createGrid">🔲 Grid Scan</button>
      <button @click="createZStack">📚 Z-Stack</button>
    </div>

    <div v-if="store.activeJobs.length > 0" class="job-list">
      <h3>Active Jobs</h3>
      <div v-for="job in store.activeJobs" :key="job.id" class="job-item">
        <div class="job-info">
          <strong>{{ job.name }}</strong>
          <span class="job-type">{{ job.job_type }}</span>
        </div>
        <div class="job-progress">
          <div class="progress-bar">
            <div
              class="progress-fill"
              :style="{ width: `${(job.progress / (job.total_steps || 1)) * 100}%` }"
            ></div>
          </div>
          <span class="progress-text">{{ job.progress }}/{{ job.total_steps }}</span>
        </div>
        <div class="job-actions">
          <button @click="pauseJob(job.id)" v-if="job.status === 'running'" class="small">Pause</button>
          <button @click="resumeJob(job.id)" v-if="job.status === 'paused'" class="small">Resume</button>
          <button @click="cancelJob(job.id)" class="small danger">Cancel</button>
        </div>
      </div>
    </div>
    <div v-else class="no-jobs">
      <p>No active jobs</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useMicroscopeStore } from '@/stores/microscope'
import { jobAPI } from '@/api/client'
import type { JobCreate } from '@/types'

const store = useMicroscopeStore()

async function createJob(job: JobCreate) {
  try {
    const created = await jobAPI.createJob(job)
    store.addJob(created)
    store.addLog(`Job created: ${job.name}`, 'success')
  } catch (error: any) {
    store.addLog(`Job creation failed: ${error.message}`, 'error')
  }
}

async function createTimelapse() {
  await createJob({
    name: 'Test Timelapse',
    job_type: 'timelapse',
    parameters: {
      interval: 5,
      duration: 60,
      exposure: 100,
      gain: 1.0
    }
  })
}

async function createGrid() {
  await createJob({
    name: 'Test Grid Scan',
    job_type: 'grid',
    parameters: {
      start_x: 0,
      end_x: 500,
      step_x: 100,
      start_y: 0,
      end_y: 500,
      step_y: 100,
      z_position: 0,
      exposure: 100,
      gain: 1.0
    }
  })
}

async function createZStack() {
  await createJob({
    name: 'Test Z-Stack',
    job_type: 'zstack',
    parameters: {
      x_position: 0,
      y_position: 0,
      start_z: 0,
      end_z: 200,
      step_z: 50,
      exposure: 100,
      gain: 1.0
    }
  })
}

async function pauseJob(jobId: number) {
  try {
    await jobAPI.updateJob(jobId, { status: 'paused' })
    store.updateJob(jobId, { status: 'paused' })
    store.addLog(`Job ${jobId} paused`, 'info')
  } catch (error: any) {
    store.addLog(`Failed to pause job: ${error.message}`, 'error')
  }
}

async function resumeJob(jobId: number) {
  try {
    await jobAPI.updateJob(jobId, { status: 'running' })
    store.updateJob(jobId, { status: 'running' })
    store.addLog(`Job ${jobId} resumed`, 'info')
  } catch (error: any) {
    store.addLog(`Failed to resume job: ${error.message}`, 'error')
  }
}

async function cancelJob(jobId: number) {
  try {
    await jobAPI.updateJob(jobId, { status: 'cancelled' })
    store.updateJob(jobId, { status: 'cancelled' })
    store.addLog(`Job ${jobId} cancelled`, 'warning')
  } catch (error: any) {
    store.addLog(`Failed to cancel job: ${error.message}`, 'error')
  }
}
</script>

<style scoped>
.job-list {
  margin-top: 15px;
}

.job-list h3 {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
}

.job-item {
  background: #f5f5f5;
  padding: 12px;
  border-radius: 4px;
  margin-bottom: 10px;
}

.job-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.job-type {
  background: #2196F3;
  color: white;
  padding: 2px 8px;
  border-radius: 3px;
  font-size: 12px;
}

.job-progress {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background: #ddd;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #4CAF50;
  transition: width 0.3s;
}

.progress-text {
  font-size: 12px;
  color: #666;
  min-width: 60px;
}

.job-actions {
  display: flex;
  gap: 5px;
}

.job-actions button {
  flex: 1;
  padding: 6px 12px;
  font-size: 12px;
}

.no-jobs {
  text-align: center;
  padding: 20px;
  color: #999;
}
</style>
