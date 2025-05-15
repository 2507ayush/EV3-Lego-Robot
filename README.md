# LEGO EV3 Night Vision Security Patrolling Rover!

## 🚀 Project Overview

This repository contains the code and design for a LEGO Mindstorms EV3 robot model integrated with **SLAM (Simultaneous Localization and Mapping)**. The rover is designed for **night vision security patrolling** and is built for reliable navigation in a known environment.

The robot is built on an **EV3 brick** and features:
- A **UV sensor** for low-light/night vision capabilities.
- **Two large motors** for mobility.
- **Wi-Fi module** with **SSH connectivity** for wireless control and communication.

## 🧠 Key Features

### ✅ SLAM Integration
- Utilizes SLAM for real-time **localization and mapping**.
- Allows the robot to understand and navigate its surroundings autonomously.

### ✅ Wireless Control via SSH
- Seamless integration with SSH over Wi-Fi for remote control and data access.
- Removes the need for tethered USB connections during operation.

### ✅ Night Vision Capability
- UV sensor enables the rover to perceive its environment even in dark conditions.
- Makes it ideal for **night-time surveillance** tasks.

### ✅ Pre-Set Path Navigation
- Can follow pre-defined paths efficiently within mapped environments.
- Ensures safe and repeatable patrol routes.

## 🛠️ Hardware Components

- **EV3 Brick** – Central controller of the robot.
- **2x Large Motors** – Primary movement actuators.
- **UV Sensor** – Enables detection in low-light scenarios.
- **Wi-Fi Module** – Provides wireless connectivity for SSH communication.

## 🧾 Software Stack

- **Python (ev3dev)** – Main programming language and platform.
- **SLAM Algorithm** – Used for real-time mapping and localization.
- **SSH over Wi-Fi** – Enables wireless command execution and monitoring.
- **LEGO Mindstorms Education Driver** - Used for accessing the Ev3 Environment on our System.

## 🔍 Application

This robot is ideal for:
- **Night Vision Security Patrolling**: Monitors pre-defined areas during night-time or in low-visibility conditions.
- **Autonomous Navigation in Indoor Environments**: Efficient movement through previously mapped spaces.

## 🔮 Future Work

- 🛞 **Enhanced Mobility**: Adding **two additional large motorized wheels** at the rear to improve traction and mobility.
- 🔊 **Sound Sensor Integration**: For detecting unusual sounds or potential intruders, enhancing the security application.
- 🧠 **AI-Based Threat Detection**: Implement object recognition and threat classification models.

## 📁 Repository Structure


## 📌 Getting Started

### Requirements
- EV3 brick with ev3dev OS
- Python environment with SLAM support
- Wi-Fi module setup for SSH
- UV sensor and motor drivers

### Setup
1. Clone this repository:
   ```bash
    git clone https://github.com/2507ayush/EV3-Lego-Robot.git

2.ssh robot@<EV3_IP_ADDRESS>

3.cd src/
python3 main.py


For running all the designated codes on the Ev3 Brick do connect the wifi module ssh with your Laptop/PC and than debug the above main.py file on to the Ev3 brick and your Rover will start move in the designated Direction.

---

## 🙏 Thank You

Thank you for taking the time to explore this project. Your interest and support mean a lot! If you have any feedback, suggestions, or ideas for collaboration, feel free to reach out. Let’s build smarter and safer robotics together!

Ayushman Verma 
GLA University, Mathura
E-mail - vermamaan55@gmail.com
Phone - 8532080960
LinkedIn - https://www.linkedin.com/in/ayushman-verma-0791752a8/
Github - @2507ayush

