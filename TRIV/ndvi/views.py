from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import NDVIRecord
from .serializers import NDVIRecordSerializer
from .utils import fetch_agro_ndvi_data
from datetime import datetime, timezone
from rest_framework import status

@api_view(['POST'])
def ndvi_history(request):
    # Extract data from the request body
    polygon_id = request.data.get('polygon_id')
    start_date_str = request.data.get('start_date')
    end_date_str = request.data.get('end_date')
    
    # Validate that start_date and end_date are provided
    if not start_date_str or not end_date_str:
        return Response({'error': 'Both start_date and end_date are required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Convert the string dates to datetime objects
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        return Response({'error': 'Invalid date format. Please use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

    # Fetch data from Agromonitoring API
    api_data = fetch_agro_ndvi_data(polygon_id, start_date_str, end_date_str)
    
    if "error" in api_data:
        return Response({'error': api_data.get('error', 'Unknown error')}, status=status.HTTP_400_BAD_REQUEST)

    # Process data and store it in the database if it's not already present
    for record in api_data:
        # Ensure the timestamp is present in the record
        timestamp = record.get('dt')  # Use 'dt' as timestamp
        if timestamp is None:
            continue  # Skip if there's no timestamp

        # Convert timestamp to datetime object
        date = datetime.utcfromtimestamp(timestamp).date()

        # Extract NDVI values
        mean_ndvi = record['data'].get('mean')
        min_ndvi = record['data'].get('min')
        max_ndvi = record['data'].get('max')
        std_ndvi = record['data'].get('std')

        # Avoid redundant data by checking for existing records
        if not NDVIRecord.objects.filter(polygon_id=polygon_id, date=date).exists():
            try:
                NDVIRecord.objects.create(
                    polygon_id=polygon_id,
                    date=date,
                    mean_ndvi=mean_ndvi,
                    min_ndvi=min_ndvi,
                    max_ndvi=max_ndvi,
                    std_ndvi=std_ndvi
                )
                print(f"Saved record for {polygon_id} on {date}")
            except Exception as e:
                print(f"Error saving record for {polygon_id} on {date}: {e}")

    # Return data from the database for the specified date range
    records = NDVIRecord.objects.filter(
        polygon_id=polygon_id,
        date__range=[start_date, end_date]
    )

    # Serialize the records and return the response
    serializer = NDVIRecordSerializer(records, many=True)
    return Response(serializer.data)
