
# **TRIV (Trends and Realtime Interactive Visualization)**

TRIV is a cutting-edge solution designed to revolutionize precision farming through real-time data collection, processing, and visualization. Leveraging advanced technologies like **3D data visualization**, **real-time streaming**, and **on-demand insights**, TRIV empowers farmers and agricultural researchers to make data-driven decisions for improved crop health and yield.

---

## **Features**

### 🌱 **Real-Time Data Collection**
- Integrates with the Agromonitoring satellite data api to fetch **soil and vegetation indices** (e.g., NDVI).
- Streams real-time soil and vegetation data using **Kafka**.

### 📊 **Interactive 3D Visualization**
- Utilizes **three.js** for 3D chart rendering, offering intuitive and interactive data exploration.
- Visualizes complex agricultural datasets for enhanced precision and understanding.

### 📡 **Real-Time Updates**
- Powered by **WebSockets** to deliver live updates for soil health and vegetation conditions.
- Implements **Kafka Streams** for high-throughput, low-latency data processing.

### 🌍 **Polygon-Based Data Handling**
- Currently supports a single polygon for data collection and analysis, with plans for user-defined polygons in future updates.

### 🚀 **Scalability & Performance**
- Deployed in a Dockerized environment with **NGINX** as a reverse proxy for optimal performance.
- Designed to handle high volumes of data while maintaining responsiveness.

---

## **Tech Stack**

- **Backend**: Django, Django Channels, Django Rest Framework
- **Frontend**: HTML, CSS, JavaScript, three.js  
- **Database**: PostgreSQL  
- **Real-Time Streaming**: Kafka, WebSockets  
- **Deployment**: Docker, NGINX  

---

## **Setup Instructions**

### **Prerequisites**
Ensure you have the following installed:
- Docker & Docker Compose  
- Python 3.10+  
- Kafka  
- PostgreSQL with PostGIS  

### **Steps**
1. Clone the repository:
   ```bash
   git clone https://github.com/vtbossss/triv.git
   cd TRIV
   cd triv
   ```

2. Build and start the Docker containers:
   ```bash
   docker-compose up --build
   ```

3. Access the application:
   - Backend: `http://localhost:8000, 80`
   - Frontend: `Html_Frontend/index.html`

---

### **Real-Time Streaming**
- WebSocket endpoint: `ws://localhost/ws/data/`

---

## **Future Enhancements**
- Support for user-defined polygons.  
- Integration with weather forecasting APIs.  
- Improved user interface with interactive tools.  
- Advanced role-based access control (RBAC).  

---

## **Contributors**
- **Vaibhav Tiwari** (Backend)  
- **Brijgopal Dalmia** (Frontend)
- **Susmit Yadav** (3d Visualization) 

---

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Contact**
For any queries, reach out via [GitHub Issues](https://github.com/vtbossss/triv/issues) or connect with me on [GitHub](https://github.com/vtbossss).

---
