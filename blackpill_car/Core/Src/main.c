/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2023 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
TIM_HandleTypeDef htim1;

UART_HandleTypeDef huart2;
DMA_HandleTypeDef hdma_usart2_rx;

/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_DMA_Init(void);
static void MX_TIM1_Init(void);
static void MX_USART2_UART_Init(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
uint8_t data[8] = {0};
uint32_t  last_control_time = 0;


//void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
//{
//  TIM1->CCR1 = data[0];
//  //TIM1->CCR2 = data[1];
//  //TIM1->CCR3 = data[2];
//  //TIM1->CCR4 = data[3];
//  HAL_UART_Receive_IT(&huart2, data, sizeof(data));
//}

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
	TIM1->CCR1 = data[0];
	TIM1->CCR2 = data[1];
	TIM1->CCR3 = data[2];
	TIM1->CCR4 = data[3];

	// engine 1
	if (data[4] == 2)
	{
	    HAL_GPIO_WritePin(d1_in1_GPIO_Port, d1_in1_Pin, GPIO_PIN_SET);
	    HAL_GPIO_WritePin(d1_in2_GPIO_Port, d1_in2_Pin, GPIO_PIN_RESET);
	}
	else if (data[4] == 1)
	{
	    HAL_GPIO_WritePin(d1_in1_GPIO_Port, d1_in1_Pin, GPIO_PIN_RESET);
	    HAL_GPIO_WritePin(d1_in2_GPIO_Port, d1_in2_Pin, GPIO_PIN_SET);
	}
	else
	{
	    HAL_GPIO_WritePin(d1_in1_GPIO_Port, d1_in1_Pin, GPIO_PIN_RESET);
	    HAL_GPIO_WritePin(d1_in2_GPIO_Port, d1_in2_Pin, GPIO_PIN_RESET);
	}

	// engine 2
	if (data[5] == 2)
	{
	    HAL_GPIO_WritePin(d1_in3_GPIO_Port, d1_in3_Pin, GPIO_PIN_SET);
	    HAL_GPIO_WritePin(d1_in4_GPIO_Port, d1_in4_Pin, GPIO_PIN_RESET);
	}
	else if (data[5] == 1)
	{
	    HAL_GPIO_WritePin(d1_in3_GPIO_Port, d1_in3_Pin, GPIO_PIN_RESET);
	    HAL_GPIO_WritePin(d1_in4_GPIO_Port, d1_in4_Pin, GPIO_PIN_SET);
	}
	else
	{
	    HAL_GPIO_WritePin(d1_in3_GPIO_Port, d1_in3_Pin, GPIO_PIN_RESET);
	    HAL_GPIO_WritePin(d1_in4_GPIO_Port, d1_in4_Pin, GPIO_PIN_RESET);
	}

	// engine 3
	if (data[6] == 2)
	{
	    HAL_GPIO_WritePin(d2_in1_GPIO_Port, d2_in1_Pin, GPIO_PIN_SET);
	    HAL_GPIO_WritePin(d2_in2_GPIO_Port, d2_in2_Pin, GPIO_PIN_RESET);
	}
	else if (data[6] == 1)
	{
	    HAL_GPIO_WritePin(d2_in1_GPIO_Port, d2_in1_Pin, GPIO_PIN_RESET);
	    HAL_GPIO_WritePin(d2_in2_GPIO_Port, d2_in2_Pin, GPIO_PIN_SET);
	}
	else
	{
	    HAL_GPIO_WritePin(d2_in1_GPIO_Port, d2_in1_Pin, GPIO_PIN_RESET);
	    HAL_GPIO_WritePin(d2_in2_GPIO_Port, d2_in2_Pin, GPIO_PIN_RESET);
	}

	// engine 4
	if (data[7] == 2)
	{
	    HAL_GPIO_WritePin(d2_in3_GPIO_Port, d2_in3_Pin, GPIO_PIN_SET);
	    HAL_GPIO_WritePin(d2_in4_GPIO_Port, d2_in4_Pin, GPIO_PIN_RESET);
	}
	else if (data[7] == 1)
	{
	    HAL_GPIO_WritePin(d2_in3_GPIO_Port, d2_in3_Pin, GPIO_PIN_RESET);
	    HAL_GPIO_WritePin(d2_in4_GPIO_Port, d2_in4_Pin, GPIO_PIN_SET);
	}
	else
	{
	    HAL_GPIO_WritePin(d2_in3_GPIO_Port, d2_in3_Pin, GPIO_PIN_RESET);
	    HAL_GPIO_WritePin(d2_in4_GPIO_Port, d2_in4_Pin, GPIO_PIN_RESET);
	}

	last_control_time = HAL_GetTick();
	HAL_UART_Receive_DMA(&huart2, data, sizeof(data));
}

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_DMA_Init();
  MX_TIM1_Init();
  MX_USART2_UART_Init();
  /* USER CODE BEGIN 2 */
  HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_1);
  HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_2);
  HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_3);
  HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_4);
  TIM1->CCR1 = 0;
  TIM1->CCR2 = 0;
  TIM1->CCR3 = 0;
  TIM1->CCR4 = 0;
  HAL_GPIO_WritePin(d1_in1_GPIO_Port, d1_in1_Pin, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(d1_in2_GPIO_Port, d1_in2_Pin, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(d1_in3_GPIO_Port, d1_in3_Pin, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(d1_in4_GPIO_Port, d1_in4_Pin, GPIO_PIN_RESET);

  HAL_GPIO_WritePin(d2_in1_GPIO_Port, d2_in1_Pin, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(d2_in2_GPIO_Port, d2_in2_Pin, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(d2_in3_GPIO_Port, d2_in3_Pin, GPIO_PIN_RESET);
  HAL_GPIO_WritePin(d2_in4_GPIO_Port, d2_in4_Pin, GPIO_PIN_RESET);

  //HAL_UART_Receive_IT (&huart2, data, sizeof(data));
  HAL_UART_Receive_DMA(&huart2, data, sizeof(data));

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_HSI;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief TIM1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM1_Init(void)
{

  /* USER CODE BEGIN TIM1_Init 0 */

  /* USER CODE END TIM1_Init 0 */

  TIM_ClockConfigTypeDef sClockSourceConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};
  TIM_OC_InitTypeDef sConfigOC = {0};
  TIM_BreakDeadTimeConfigTypeDef sBreakDeadTimeConfig = {0};

  /* USER CODE BEGIN TIM1_Init 1 */

  /* USER CODE END TIM1_Init 1 */
  htim1.Instance = TIM1;
  htim1.Init.Prescaler = 64;
  htim1.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim1.Init.Period = 255;
  htim1.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim1.Init.RepetitionCounter = 0;
  htim1.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_Base_Init(&htim1) != HAL_OK)
  {
    Error_Handler();
  }
  sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
  if (HAL_TIM_ConfigClockSource(&htim1, &sClockSourceConfig) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_TIM_PWM_Init(&htim1) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim1, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sConfigOC.OCMode = TIM_OCMODE_PWM1;
  sConfigOC.Pulse = 0;
  sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
  sConfigOC.OCNPolarity = TIM_OCNPOLARITY_HIGH;
  sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
  sConfigOC.OCIdleState = TIM_OCIDLESTATE_RESET;
  sConfigOC.OCNIdleState = TIM_OCNIDLESTATE_RESET;
  if (HAL_TIM_PWM_ConfigChannel(&htim1, &sConfigOC, TIM_CHANNEL_1) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_TIM_PWM_ConfigChannel(&htim1, &sConfigOC, TIM_CHANNEL_2) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_TIM_PWM_ConfigChannel(&htim1, &sConfigOC, TIM_CHANNEL_3) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_TIM_PWM_ConfigChannel(&htim1, &sConfigOC, TIM_CHANNEL_4) != HAL_OK)
  {
    Error_Handler();
  }
  sBreakDeadTimeConfig.OffStateRunMode = TIM_OSSR_DISABLE;
  sBreakDeadTimeConfig.OffStateIDLEMode = TIM_OSSI_DISABLE;
  sBreakDeadTimeConfig.LockLevel = TIM_LOCKLEVEL_OFF;
  sBreakDeadTimeConfig.DeadTime = 0;
  sBreakDeadTimeConfig.BreakState = TIM_BREAK_DISABLE;
  sBreakDeadTimeConfig.BreakPolarity = TIM_BREAKPOLARITY_HIGH;
  sBreakDeadTimeConfig.AutomaticOutput = TIM_AUTOMATICOUTPUT_DISABLE;
  if (HAL_TIMEx_ConfigBreakDeadTime(&htim1, &sBreakDeadTimeConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM1_Init 2 */

  /* USER CODE END TIM1_Init 2 */
  HAL_TIM_MspPostInit(&htim1);

}

/**
  * @brief USART2 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART2_UART_Init(void)
{

  /* USER CODE BEGIN USART2_Init 0 */

  /* USER CODE END USART2_Init 0 */

  /* USER CODE BEGIN USART2_Init 1 */

  /* USER CODE END USART2_Init 1 */
  huart2.Instance = USART2;
  huart2.Init.BaudRate = 115200;
  huart2.Init.WordLength = UART_WORDLENGTH_8B;
  huart2.Init.StopBits = UART_STOPBITS_1;
  huart2.Init.Parity = UART_PARITY_NONE;
  huart2.Init.Mode = UART_MODE_TX_RX;
  huart2.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart2.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart2) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART2_Init 2 */

  /* USER CODE END USART2_Init 2 */

}

/**
  * Enable DMA controller clock
  */
static void MX_DMA_Init(void)
{

  /* DMA controller clock enable */
  __HAL_RCC_DMA1_CLK_ENABLE();

  /* DMA interrupt init */
  /* DMA1_Stream5_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(DMA1_Stream5_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(DMA1_Stream5_IRQn);

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};
/* USER CODE BEGIN MX_GPIO_Init_1 */
/* USER CODE END MX_GPIO_Init_1 */

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOC, d1_in1_Pin|d1_in2_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOB, d2_in4_Pin|d2_in3_Pin|d2_in1_Pin|d2_in2_Pin
                          |d1_in4_Pin|d1_in3_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pins : d1_in1_Pin d1_in2_Pin */
  GPIO_InitStruct.Pin = d1_in1_Pin|d1_in2_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

  /*Configure GPIO pins : d2_in4_Pin d2_in3_Pin d2_in1_Pin d2_in2_Pin
                           d1_in4_Pin d1_in3_Pin */
  GPIO_InitStruct.Pin = d2_in4_Pin|d2_in3_Pin|d2_in1_Pin|d2_in2_Pin
                          |d1_in4_Pin|d1_in3_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

/* USER CODE BEGIN MX_GPIO_Init_2 */
/* USER CODE END MX_GPIO_Init_2 */
}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
