from django.shortcuts import render

import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from django.shortcuts import get_object_or_404
from user.models import User
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Dimension, Metric
from .serializers import UserSerializer, UserCreateUpdateSerializer



# Set up logging
logger = logging.getLogger('User')


class UserListView(APIView):

    def get(self, request):

          # Log the request
        logger.info("Received request to list all users")

        # Retrieve all users from the database
        users = User.objects.all()

        #serialise the user data
        serializer = UserSerializer(users, many=True)

        # Log the number of users retrieved
        logger.info(f"Returning {len(users)} users")

         # Return the serialized user data
        return Response(serializer.data)

    def post(self, request):
        # Log the request
        logger.info("Received request to create a new user")

        # Deserialize the request data
        serializer = UserCreateUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            # Save the new user
            user = serializer.save()

            # Log the creation of the new user
            logger.info(f"User created with ID {user.id}")

            # Return the serialized user data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Log the validation errors
            logger.error(f"User creation failed: {serializer.errors}")

            # Return validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserDetailView(APIView):
    
    def get(self, request, user_id):
        # Log the request with user_id
        logger.info(f"Received request to retrieve details for user ID {user_id}")

        # Retrieve the specific user or return a 404 error if not found
        user = get_object_or_404(User, user_id=user_id)

        # Serialize the user data
        serializer = UserSerializer(user)

        # Log the user details being returned
        logger.info(f"Returning details for user ID {user_id}")

        # Return the serialized user data
        return Response(serializer.data)


    def put(self, request, user_id):

        # Log the request with user_id
        logger.info(f"Received request to update user with ID {user_id}")

        # Retrieve the specific user or return a 404 error if not found
        user = get_object_or_404(User, id=user_id)

        # Deserialize the request data for updating user
        serializer = UserCreateUpdateSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():

            # Save the updated user data
            user = serializer.save()

            # Log the update of the user
            logger.info(f"User with ID {user.id} has been updated successfully")

            # Return the serialized user data
            return Response(serializer.data)

        else:

            # Log the validation errors
            logger.error(f"User update failed: {serializer.errors}")

            # Return validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    
    def delete(self, request, user_id):
        logger.info("Deleting user with ID: %s", id)

        try:
            user = User.objects.get(user_id=user_id, is_updated=False)
            user.soft_delete()
            logger.info("User with ID %s deleted successfully.", id)
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            logger.warning("User with ID%s not found for deletion.", id)
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    

    def restore(self, request, user_id):
        logger.info("Restoring user with ID: %s", id)
        try:
            user = User.objects.get(id=id, is_updated=True)
            user.restore()
            logger.info("User with ID %s restored successfully.", id)
            return Response({'message': 'User restored successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            logger.warning("User with ID %s not found for restoration.", id)
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)



class UserMetricsView(APIView):
    def get(self, request):
        # Log the request
        logger.info("Received request for user metrics")

        # Calculate metrics
        total_users = self.get_total_users()
        active_users = self.get_active_users()
        retention_rate = self.get_retention_rate()

        # Log the calculated metrics
        logger.info(f"User metrics: total_users = {total_users}, active_users = {active_users}, retention_rate = {retention_rate:.2f}%")

        # Return the metrics
        return Response({
            'total_users': total_users,
            'active_users': active_users,
            'retention_rate': retention_rate
        })

    def get_total_users(self):
        # Return the total number of users
        total_users = User.objects.count()
        return total_users

    def get_active_users(self):
        # Active user is one who has logged in within the last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)
        active_users = User.objects.filter(last_login__gte=thirty_days_ago).count()
        return active_users

    def get_retention_rate(self):
        
        # Retention rate is the percentage of users active in the last 30 days relative to the total users
        total_users = self.get_total_users()
        active_users = self.get_active_users()
        if total_users == 0:
            return 0.0 
        retention_rate = (active_users / total_users) * 100
        return retention_rate


class ResourceUsageView(APIView):
    def get(self, request):

        # Log the request
        logger.info("Received request for resource usage metrics from Google Analytics")
        
        # Get the resource path from the query parameters
        resource_path = request.query_params.get('resource_path')
        
        if not resource_path:
            logger.error("No resource_path provided in the request")
            return Response({"error": "resource_path is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Set up Google Analytics Data API v1 client
            client = BetaAnalyticsDataClient()

            # Set the date range for the last 30 days
            end_date = timezone.now().date()
            start_date = end_date - timezone.timedelta(days=30)

            # Construct the RunReportRequest
            request = RunReportRequest(
                property=f"properties/{settings.GA4_PROPERTY_ID}",
                date_ranges=[DateRange(start_date=start_date.isoformat(), end_date=end_date.isoformat())],
                dimensions=[Dimension(name="pagePath")],
                metrics=[
                    Metric(name="screenPageViews"),
                    Metric(name="averageSessionDuration"),
                    Metric(name="eventCount")
                ],
                dimension_filter={
                    "filter": {
                        "field_name": "pagePath",
                        "string_filter": {
                            "value": resource_path
                        }
                    }
                }
            )

            # Run the report
            response = client.run_report(request)

            # Process the response
            if len(response.rows) > 0:
                row = response.rows[0]
                page_views = int(row.metric_values[0].value)
                avg_session_duration = float(row.metric_values[1].value)
                event_count = int(row.metric_values[2].value)
                
                usage_data = {
                    'resource_path': resource_path,
                    'total_views': page_views,
                    'avg_time_spent': round(avg_session_duration, 2),  # in seconds
                    'total_events': event_count
                }
            else:
                usage_data = {
                    'resource_path': resource_path,
                    'total_views': 0,
                    'avg_time_spent': 0,
                    'total_events': 0
                }
            
            # Log the fetched usage data
            logger.info(f"Fetched resource usage data from Google Analytics: {usage_data}")
            
            # Return the usage data
            return Response(usage_data)
        
        except Exception as e:
            # Log any errors that occur during the process
            logger.error(f"Error fetching resource usage from Google Analytics: {str(e)}")
            return Response({"error": "An error occurred while fetching resource usage"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


