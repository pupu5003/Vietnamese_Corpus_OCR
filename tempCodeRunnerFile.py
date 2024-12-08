                    # if cnt != word_count_ground:
                    #     if word and abs(word[0][0][0][0]) > first_word_distance:
                    #         x_start = 0
                    #         x_end = int(word[0][0][0][0])
                    #         y_start = 0
                    #         y_end = int(cropped_image_1.shape[0])
                    #         # Crop the space between the two boxes
                    #         cropped_space = cropped_image_1[y_start:y_end, x_start:x_end]

                    #         # Save the cropped space
                    #         if cropped_space is not None and cropped_space.size > 0:
                    #             cnt = cnt + 1
                    #             tmp_cnt = tmp_cnt + 1
                    #             cropped_space_temp_path = os.path.join(new_file, f'temp_cropped_space_{tmp_cnt:03}.png')
                    #             cv2.imwrite(cropped_space_temp_path, cropped_space)
                    #             # Insert the image at the correct position in the folder
                    #             shift_and_insert_image(new_file, cropped_space_temp_path, 1)
                    #             os.remove(cropped_space_temp_path)  # Clean up temporary file

                    #     # Last word
                    #     if word and abs(word[len(word)-1][0][1][0] - cropped_image_1.shape[1]) > last_word_distance:
                    #         x_start = int(word[len(word)-1][0][1][0])
                    #         x_end = int(cropped_image_1.shape[1])
                    #         y_start = 0
                    #         y_end = int(cropped_image_1.shape[0])
                    #         # Crop the space between the two boxes
                    #         cropped_space = cropped_image_1[y_start:y_end, x_start:x_end]

                    #         # Save the cropped space
                    #         if cropped_space is not None and cropped_space.size > 0:
                    #             cnt = cnt + 1
                    #             tmp_cnt = tmp_cnt + 1
                    #             cropped_space_temp_path = os.path.join(new_file, f'temp_cropped_space_{tmp_cnt:03}.png')
                    #             cv2.imwrite(cropped_space_temp_path, cropped_space)
                    #             # print(f"Temporary cropped space image saved at {cropped_space_temp_path}")
                    #             file_count = len([f for f in os.listdir(new_file) if os.path.isfile(os.path.join(new_file, f))])
                    #             shift_and_insert_image(new_file, cropped_space_temp_path, file_count)
                    #             os.remove(cropped_space_temp_path)  # Clean up temporary file
                     